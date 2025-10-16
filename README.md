# LLM Code Deployer

A FastAPI-based deployment service that provides endpoints for building and revising code projects via API requests. This service validates requests using email and secret authentication.

## Features

- **POST /build** - Build and deploy code projects
- **POST /revise** - Revise existing deployments
- Email and secret-based authentication
- Input validation for all requests
- RESTful API design
- MIT Licensed

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

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

3. Run the FastAPI application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Build Endpoint

**POST** `/build`

Request body:
```json
{
  "email": "user@example.com",
  "secret": "your-secret-key",
  "project_name": "my-project",
  "code": "# your code here"
}
```

Response:
```json
{
  "status": "success",
  "message": "Build completed successfully",
  "project_id": "abc123"
}
```

### Revise Endpoint

**POST** `/revise`

Request body:
```json
{
  "email": "user@example.com",
  "secret": "your-secret-key",
  "project_id": "abc123",
  "changes": "description of changes"
}
```

Response:
```json
{
  "status": "success",
  "message": "Revision completed successfully"
}
```

## Deployment

### GitHub Pages Deployment

This repository is configured for GitHub Pages deployment from the `main` branch.

1. Go to **Settings** > **Pages**
2. Select **Source**: Deploy from a branch
3. Select **Branch**: main, folder: / (root)
4. Click **Save**

The site will be available at:
```
https://manthan-bumb.github.io/llm-code-deployer/
```

### API Documentation

Once deployed, you can access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
llm-code-deployer/
├── main.py              # FastAPI application with endpoints
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── LICENSE             # MIT License
```

## Authentication

All API endpoints require:
- **email**: A valid email address
- **secret**: A secret key for authentication

Both fields are validated on each request.

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (invalid credentials)
- `500`: Internal Server Error

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository URLs

- **Repository**: https://github.com/Manthan-Bumb/llm-code-deployer
- **GitHub Pages**: https://manthan-bumb.github.io/llm-code-deployer/

## Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.
