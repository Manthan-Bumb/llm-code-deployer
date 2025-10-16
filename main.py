from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import re

app = FastAPI(
    title="LLM Code Deployer",
    description="A FastAPI service for building and revising code projects with email and secret authentication",
    version="1.0.0"
)

# Request Models
class BuildRequest(BaseModel):
    email: EmailStr = Field(..., description="Valid email address for authentication")
    secret: str = Field(..., min_length=8, description="Secret key for authentication (minimum 8 characters)")
    project_name: str = Field(..., min_length=1, max_length=100, description="Name of the project to build")
    code: str = Field(..., min_length=1, description="Source code to build")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "secret": "your-secret-key",
                "project_name": "my-project",
                "code": "print('Hello, World!')"
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

class ReviseResponse(BaseModel):
    status: str
    message: str

# Helper function to validate authentication
def validate_auth(email: str, secret: str) -> bool:
    """
    Validate email and secret.
    In production, this would check against a database.
    """
    # Basic validation - secret must be at least 8 characters
    if len(secret) < 8:
        return False
    
    # Email is already validated by EmailStr, but we can add additional checks
    if not email or '@' not in email:
        return False
    
    return True

@app.get("/")
async def root():
    """
    Root endpoint providing API information
    """
    return {
        "name": "LLM Code Deployer",
        "version": "1.0.0",
        "status": "active",
        "endpoints": [
            {
                "path": "/build",
                "method": "POST",
                "description": "Build and deploy a code project"
            },
            {
                "path": "/revise",
                "method": "POST",
                "description": "Revise an existing project"
            },
            {
                "path": "/docs",
                "method": "GET",
                "description": "Interactive API documentation (Swagger UI)"
            },
            {
                "path": "/redoc",
                "method": "GET",
                "description": "API documentation (ReDoc)"
            }
        ]
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "llm-code-deployer"}

@app.post("/build", response_model=BuildResponse, status_code=status.HTTP_201_CREATED)
async def build_project(request: BuildRequest):
    """
    Build and deploy a code project.
    
    Validates email and secret, then processes the build request.
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
    
    # Generate a simple project ID (in production, use UUID or database ID)
    project_id = f"{request.project_name}-{hash(request.email) % 100000}"
    
    # In production, this would:
    # 1. Store the project in a database
    # 2. Build/compile the code
    # 3. Deploy to a hosting service
    # 4. Return deployment URLs
    
    return BuildResponse(
        status="success",
        message=f"Build completed successfully for project '{request.project_name}'",
        project_id=project_id
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
