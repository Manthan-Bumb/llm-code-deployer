from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import re
import os
import requests
import base64
import json

# Initialize FastAPI app
app = FastAPI(
    title="LLM Code Deployer",
    description="A FastAPI service for building and deploying code projects to GitHub with email and secret authentication",
    version="2.0.0"
)

# GitHub Token from environment variable
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required")

GITHUB_API_URL = "https://api.github.com"

# Request Models
class BuildRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address for authentication")
    secret: str = Field(..., min_length=8, description="Secret key for authentication (minimum 8 characters)")
    project_name: str = Field(..., min_length=1, max_length=100, description="Name of the project to build")
    code: str = Field(..., min_length=1, description="Source code to build")
    github_username: str = Field(..., description="GitHub username for repository creation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "secret": "your-secret-key",
                "project_name": "my-project",
                "code": "print('Hello, World!')",
                "github_username": "your-github-username"
            }
        }

class ReviseRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address for authentication")
    secret: str = Field(..., min_length=8, description="Secret key for authentication (minimum 8 characters)")
    project_id: str = Field(..., min_length=1, description="ID of the project to revise")
    changes: str = Field(..., min_length=1, description="Description of changes to make")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "secret": "your-secret-key",
                "project_id": "abc123",
                "changes": "Update the greeting message"
            }
        }

# Response Models
class BuildResponse(BaseModel):
    status: str
    message: str
    project_id: str
    repository_url: Optional[str] = None
    pages_url: Optional[str] = None

class ReviseResponse(BaseModel):
    status: str
    message: str

# Helper function to validate authentication
def validate_auth(email: str, secret: str) -> bool:
    """
    Validate email and secret.
    In production, this would check against a database.
    For now, basic validation (email format already validated by EmailStr).
    """
    # Simple validation - in production, check against database
    return len(secret) >= 8 and '@' in email

# GitHub API helper functions
def create_github_repo(repo_name: str, username: str) -> dict:
    """
    Create a new GitHub repository using the GitHub API.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": repo_name,
        "description": f"LLM Code Deployer project: {repo_name}",
        "private": False,
        "auto_init": True
    }
    
    response = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create GitHub repository: {response.text}"
        )

def push_code_to_github(repo_name: str, username: str, code: str, filename: str = "main.py") -> dict:
    """
    Push code to GitHub repository.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Encode content to base64
    content_encoded = base64.b64encode(code.encode()).decode()
    
    data = {
        "message": f"Add {filename}",
        "content": content_encoded
    }
    
    response = requests.put(
        f"{GITHUB_API_URL}/repos/{username}/{repo_name}/contents/{filename}",
        headers=headers,
        json=data
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to push code to GitHub: {response.text}"
        )

def enable_github_pages(repo_name: str, username: str) -> dict:
    """
    Enable GitHub Pages for the repository.
    """
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    
    response = requests.post(
        f"{GITHUB_API_URL}/repos/{username}/{repo_name}/pages",
        headers=headers,
        json=data
    )
    
    if response.status_code in [200, 201, 204]:
        return {"pages_url": f"https://{username}.github.io/{repo_name}/"}
    else:
        # Pages might already be enabled or not applicable
        return {"pages_url": None}

# API Endpoints
@app.get("/")
async def root():
    return {
        "message": "LLM Code Deployer API",
        "version": "2.0.0",
        "github_integration": "enabled",
        "endpoints": ["/build", "/revise"]
    }

@app.post("/build", response_model=BuildResponse)
async def build_project(request: BuildRequest):
    """
    Build and deploy a new project to GitHub.
    
    Validates email and secret, creates a GitHub repository,
    pushes code, and enables GitHub Pages.
    """
    # Validate authentication
    if not validate_auth(request.email, request.secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or secret"
        )
    
    # Validate project name (alphanumeric, hyphens, underscores only)
    if not re.match(r'^[a-zA-Z0-9_-]+$', request.project_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project name must contain only alphanumeric characters, hyphens, and underscores"
        )
    
    # Generate a simple project ID
    project_id = f"{request.project_name}-{hash(request.email) % 100000}"
    
    try:
        # Create GitHub repository
        repo = create_github_repo(request.project_name, request.github_username)
        repo_url = repo.get("html_url")
        
        # Push code to GitHub
        push_code_to_github(request.project_name, request.github_username, request.code)
        
        # Enable GitHub Pages
        pages_info = enable_github_pages(request.project_name, request.github_username)
        pages_url = pages_info.get("pages_url")
        
        return BuildResponse(
            status="success",
            message=f"Build completed successfully for project '{request.project_name}'",
            project_id=project_id,
            repository_url=repo_url,
            pages_url=pages_url
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during build: {str(e)}"
        )

@app.post("/revise", response_model=ReviseResponse)
async def revise_project(request: ReviseRequest):
    """
    Revise an existing project.
    
    Validates email and secret, then processes the revision request.
    """
    # Validate authentication
    if not validate_auth(request.email, request.secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or secret"
        )
    
    # Validate project_id format
    if not request.project_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project ID cannot be empty"
        )
    
    # In production, this would:
    # 1. Verify project exists and user has access
    # 2. Apply the requested changes
    # 3. Rebuild/redeploy the project
    # 4. Return updated deployment information
    
    return ReviseResponse(
        status="success",
        message=f"Revision completed successfully for project '{request.project_id}'"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
