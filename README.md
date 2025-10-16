# LLM Code Deployer

A FastAPI-based deployment service that provides endpoints for building and deploying code projects to GitHub via API requests. This service validates requests using email and secret authentication and automatically creates GitHub repositories, pushes code, and enables GitHub Pages.

## Features

- **POST /build** - Build and deploy code projects to GitHub
- **POST /revise** - Revise existing deployments
- Email and secret-based authentication
- GitHub integration with Personal Access Token (PAT)
- Automatic repository creation
- Code push to GitHub
- GitHub Pages deployment
- Input validation for all requests
- RESTful API design
- MIT Licensed

## Prerequisites

- Python 3.8 or higher
- pip package manager
- GitHub account
- GitHub Personal Access Token (Classic) with `repo` and `workflow` permissions

## GitHub Token Setup

### Creating a GitHub Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a descriptive name (e.g., "llm-code-deployer API token")
4. Select the following scopes:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (Update GitHub Action workflows)
5. Click "Generate token"
6. **Important**: Copy the token immediately - you won't be able to see it again!

### Setting Up the Token as Environment Variable

The token `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` has been created with the required permissions.

#### On Linux/macOS:
```bash
export GITHUB_TOKEN="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"
```

To make it permanent, add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export GITHUB_TOKEN="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"' >> ~/.bashrc
source ~/.bashrc
```

#### On Windows (PowerShell):
```powershell
$env:GITHUB_TOKEN="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"
```

To make it permanent:
```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN','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','User')
```

#### On Windows (Command Prompt):
```cmd
set GITHUB_TOKEN=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
```

#### Using .env file (Development):

Create a `.env` file in the project root:
```env
GITHUB_TOKEN=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
```

Install python-dotenv:
```bash
pip install python-dotenv
```

Load in your code (add to `main.py`):
```python
from dotenv import load_dotenv
load_dotenv()  # Add this before accessing os.getenv("GITHUB_TOKEN")
```

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/Manthan-Bumb/llm-code-deployer.git
cd llm-code-deployer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your GitHub token (see "GitHub Token Setup" section above)

4. Verify the token is set:
```bash
echo $GITHUB_TOKEN  # Linux/macOS
echo %GITHUB_TOKEN%  # Windows CMD
echo $env:GITHUB_TOKEN  # Windows PowerShell
```

5. Run the FastAPI application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Usage

### Root Endpoint

**GET** `/`

Returns API information and available endpoints.

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "message": "LLM Code Deployer API",
  "version": "2.0.0",
  "github_integration": "enabled",
  "endpoints": ["/build", "/revise"]
}
```

### Build Endpoint

**POST** `/build`

Creates a GitHub repository, pushes code, and enables GitHub Pages.

Request body:
```json
{
  "email": "user@example.com",
  "secret": "your-secret-key",
  "project_name": "my-test-project",
  "code": "print('Hello from GitHub!')",
  "github_username": "Manthan-Bumb"
}
```

Response:
```json
{
  "status": "success",
  "message": "Build completed successfully for project 'my-test-project'",
  "project_id": "my-test-project-12345",
  "repository_url": "https://github.com/Manthan-Bumb/my-test-project",
  "pages_url": "https://Manthan-Bumb.github.io/my-test-project/"
}
```

### Revise Endpoint

**POST** `/revise`

Revises an existing project (placeholder for future implementation).

Request body:
```json
{
  "email": "user@example.com",
  "secret": "your-secret-key",
  "project_id": "my-test-project-12345",
  "changes": "Update the print statement"
}
```

Response:
```json
{
  "status": "success",
  "message": "Revision completed successfully for project 'my-test-project-12345'"
}
```

## Testing the API

### Test 1: Using cURL

```bash
curl -X POST http://localhost:8000/build \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "secret": "test-secret-key",
    "project_name": "my-test-api-project",
    "code": "<!DOCTYPE html>\n<html>\n<head><title>Test Page</title></head>\n<body><h1>Hello from LLM Code Deployer!</h1></body>\n</html>",
    "github_username": "Manthan-Bumb"
  }'
```

### Test 2: Using Python requests

```python
import requests
import json

url = "http://localhost:8000/build"

payload = {
    "email": "test@example.com",
    "secret": "test-secret-key",
    "project_name": "my-python-test-project",
    "code": "print('Hello from automated deployment!')",
    "github_username": "Manthan-Bumb"
}

response = requests.post(url, json=payload)
print(json.dumps(response.json(), indent=2))
```

### Test 3: Using the Interactive API Docs

1. Navigate to `http://localhost:8000/docs`
2. Click on "POST /build" to expand it
3. Click "Try it out"
4. Fill in the request body:
   ```json
   {
     "email": "test@example.com",
     "secret": "test-secret-key",
     "project_name": "my-interactive-test",
     "code": "console.log('Hello from interactive test!');",
     "github_username": "Manthan-Bumb"
   }
   ```
5. Click "Execute"
6. Check the response and visit the generated repository URL

## Verification Steps

After running a test build:

1. **Check GitHub Repository**:
   - Visit the `repository_url` from the response
   - Verify the repository was created
   - Check that the code file (`main.py`) exists with your content

2. **Check GitHub Pages**:
   - Visit the `pages_url` from the response
   - Note: GitHub Pages may take a few minutes to build and deploy
   - If it's HTML content, you should see it rendered

3. **Verify Token Permissions**:
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
   ```
   This should return your GitHub user information

## Troubleshooting

### "GITHUB_TOKEN environment variable is required"
- Make sure you've set the `GITHUB_TOKEN` environment variable
- Restart your terminal/IDE after setting the variable
- Verify with: `echo $GITHUB_TOKEN`

### "Failed to create GitHub repository"
- Check that your token has `repo` permissions
- Verify the token hasn't expired (check GitHub settings)
- Ensure the repository name doesn't already exist
- Check that the token is correctly set in the environment

### "Failed to push code to GitHub"
- Verify the repository was created successfully
- Check that your token has write permissions
- Ensure the code content is valid

### Repository created but Pages not enabled
- GitHub Pages may not support all repository types
- Check the repository settings manually
- Some content types require specific file structures (e.g., `index.html` for HTML sites)

## Security Best Practices

1. **Never commit your GitHub token** to version control
2. **Add `.env` to `.gitignore`** if using a `.env` file
3. **Rotate tokens regularly** - generate new tokens every few months
4. **Use minimal permissions** - only enable scopes you need
5. **Revoke unused tokens** - delete tokens you're no longer using
6. **Monitor token usage** - check GitHub settings for token activity

## Requirements

The project requires the following Python packages (in `requirements.txt`):

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
pydantic[email]>=2.4.0
requests>=2.31.0
python-dotenv>=1.0.0  # Optional, for .env file support
```

## Implementation Details

### GitHub API Functions

1. **`create_github_repo()`** - Creates a new repository using GitHub REST API
2. **`push_code_to_github()`** - Pushes code files to the repository
3. **`enable_github_pages()`** - Enables GitHub Pages for the repository

### Authentication Flow

1. Client sends request with email and secret
2. API validates credentials (basic validation in this version)
3. API uses GitHub token from environment variable for GitHub operations
4. Returns success/failure with repository information

## Future Enhancements

- [ ] Database integration for user management
- [ ] Enhanced authentication (OAuth, JWT)
- [ ] Support for multiple files in a project
- [ ] Branch management
- [ ] CI/CD pipeline integration
- [ ] WebSocket support for real-time deployment status
- [ ] Project revision functionality with GitHub commits
- [ ] Support for private repositories
- [ ] Custom domain configuration for GitHub Pages

## License

MIT License - see LICENSE file for details

## Completed Steps

✅ **Step 1**: Created GitHub Personal Access Token (Classic)
- Token: `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`
- Scopes: `repo` and `workflow`
- Expiration: 30 days (November 15, 2025)

✅ **Step 2**: Updated `main.py` with GitHub Integration
- Added environment variable support for `GITHUB_TOKEN`
- Implemented `create_github_repo()` function
- Implemented `push_code_to_github()` function
- Implemented `enable_github_pages()` function
- Updated `/build` endpoint to use GitHub API
- Added `github_username` field to BuildRequest model
- Improved error handling and response models

✅ **Step 3**: Updated README.md Documentation
- Added GitHub token setup instructions
- Documented environment variable configuration for all platforms
- Added API usage examples with GitHub integration
- Included test build instructions (cURL, Python, Interactive docs)
- Added verification steps for checking deployments
- Included troubleshooting section
- Documented security best practices

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
