# Mistral OCR Tool

A robust tool for processing documents using the Mistral OCR API. This tool can process a single file, a directory of files, or a URL, extracting text and other information using OCR technology.

## Features

- Process PDF, PNG, JPG, JPEG, TIFF, TIF, and BMP files
- Process documents from URLs
- Process multiple documents in a directory
- Save OCR results in JSON format
- Comprehensive logging system with console and file output
- Robust error handling with detailed custom exceptions
- Clean code architecture following SOLID principles and best practices
- Type-annotated codebase for better IDE support and code safety
- **REST API mode** with FastAPI and Uvicorn
- **Docker support** for easy deployment

## Installation

### Prerequisites

- Python 3.12 or higher
- Mistral API key

### Setup

1. Clone the repository:

```bash
git clone https://github.com/ShivamB25/mistral-ocr-tool.git
cd mistral-ocr-tool
```

2. Install the package using uv:

```bash
# For CLI mode only
uv pip install -e .

# For API mode (includes FastAPI and Uvicorn)
uv pip install -e '.[api]'
```

3. Create a `.env` file in the root directory with your Mistral API key:

```
MISTRAL_API_KEY="your_api_key_here"
```

## Usage

The tool can be run in two modes: CLI mode and API mode.

### CLI Mode

```bash
python main.py cli -i <input_path> -o <output_path> [-v] [-l <log_file>]
```

#### CLI Arguments

- `-i, --input`: Path to the input file or directory, or a URL (required)
- `-o, --output`: Path to the output file (required)
- `-v, --verbose`: Enable verbose logging
- `-l, --log-file`: Path to the log file

#### CLI Examples

Process a single file:

```bash
python main.py cli -i my_document.pdf -o output.json
```

Process all files in a directory:

```bash
python main.py cli -i documents/ -o output.json
```

Process a single URL:

```bash
python main.py cli -i https://arxiv.org/pdf/2201.04234 -o output.json
```

Enable verbose logging:

```bash
python main.py cli -i my_document.pdf -o output.json -v
```

Save logs to a file:

```bash
python main.py cli -i my_document.pdf -o output.json -l logs/ocr.log
```

### API Mode

Run the tool as a REST API server:

```bash
python main.py api [--host HOST] [--port PORT] [--reload] [--workers WORKERS] [--log-level {debug,info,warning,error,critical}] [--log-file LOG_FILE]
```

#### API Arguments

- `--host`: Host to bind the server to (default: 0.0.0.0)
- `--port`: Port to bind the server to (default: 8000)
- `--reload`: Enable auto-reload for development
- `--workers`: Number of worker processes (default: 1)
- `--log-level`: Logging level (default: info)
- `--log-file`: Path to the log file

#### API Examples

Run the API server with default settings:

```bash
python main.py api
```

Run the API server with custom settings:

```bash
python main.py api --host 127.0.0.1 --port 5000 --workers 4 --log-level debug
```

Run the API server with auto-reload for development:

```bash
python main.py api --reload
```

### API Endpoints

The API provides the following endpoints:

- `GET /health`: Health check endpoint
- `POST /ocr/process`: Process a single document (URL or file upload)
- `POST /ocr/batch`: Process multiple documents in batch mode

#### Example API Requests

Process a URL:

```bash
curl -X POST http://localhost:8000/ocr/process \
  -H "Content-Type: application/json" \
  -d '{"process_type": "url", "url": "https://arxiv.org/pdf/2201.04234", "include_images": false}'
```

Process a file upload:

```bash
curl -X POST http://localhost:8000/ocr/process \
  -H "Content-Type: multipart/form-data" \
  -F "file=@my_document.pdf" \
  -F "request={\"process_type\": \"file\", \"include_images\": false}"
```

Process multiple URLs in batch mode:

```bash
curl -X POST http://localhost:8000/ocr/batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://arxiv.org/pdf/2201.04234", "https://arxiv.org/pdf/2202.05262"], "include_images": false}'
```

## Docker Support

The tool can be run in a Docker container for easy deployment.

### Build and Run with Docker

1. Build the Docker image:

```bash
docker build -t mistral-ocr-api .
```

2. Run the Docker container:

```bash
docker run -p 8000:8000 -e MISTRAL_API_KEY="your_api_key_here" mistral-ocr-api
```

The Docker image is built using multi-stage builds to reduce the final image size. It also runs the application as a non-root user for security.

### Run with Docker Compose

1. Set your Mistral API key in the environment or in a `.env` file.

2. Start the services:

```bash
docker-compose up -d
```

3. Stop the services:

```bash
docker-compose down
```

## Project Structure

```
mistral-ocr-tool/
├── main.py                  # Entry point with CLI and API modes
├── ocr/                     # OCR module
│   ├── __init__.py
│   └── ocr_service.py       # OCR service with specialized processing methods
├── api/                     # API module
│   ├── __init__.py
│   ├── app.py               # FastAPI application and routes
│   ├── models.py            # Pydantic models for API requests/responses
│   └── server.py            # Uvicorn server configuration
├── utils/                   # Utility modules
│   ├── __init__.py
│   ├── api_client.py        # Mistral API client for OCR requests
│   ├── constants.py         # Well-documented constants and enumerations
│   ├── exceptions.py        # Hierarchical custom exception system
│   ├── file_handler.py      # File utilities with context managers
│   └── logger.py            # Advanced logging with configuration options
├── config/                  # Configuration
│   ├── __init__.py
│   └── settings.py          # Environment-based configuration
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Environment variables
├── pyproject.toml           # Project metadata
└── README.md                # Documentation
```

## Clean Code Principles

The codebase follows these clean code principles:

1. **Single Responsibility Principle**: Each class and function has a single, well-defined responsibility.
   - Example: The `OCRService` delegates file processing to specialized methods.

2. **DRY (Don't Repeat Yourself)**: Common functionality is extracted into reusable methods.
   - Example: File handling logic is centralized in the `FileHandler` class.

3. **Comprehensive Error Handling**: Custom exceptions with meaningful messages.
   - Example: Specific exceptions like `UnsupportedFileTypeError` provide clear error context.

4. **Defensive Programming**: Input validation and proper error handling throughout.
   - Example: The `safe_open` context manager in `FileHandler` handles file operations safely.

5. **Consistent Naming**: Clear, descriptive names for variables, functions, and classes.
   - Example: Method names like `process_documents` clearly describe their purpose.

6. **Comprehensive Documentation**: Detailed docstrings and comments.
   - Example: All public methods have docstrings with parameter descriptions and return types.

7. **Type Annotations**: Full type hinting for better IDE support and code safety.
   - Example: All function parameters and return values have type annotations.

## Error Handling

The tool includes a robust hierarchical exception system:

- `OCRToolError`: Base exception for all OCR tool errors
- `APIError`: Exception for API-related errors, includes optional status code
- `ConfigurationError`: Exception for configuration issues like missing API keys
- `FileError`: Exception for file operations, includes the problematic file path
- `UnsupportedFileTypeError`: Specialized exception for unsupported file formats
- `InvalidInputError`: Exception for invalid user input or parameters

Each exception provides detailed context about the error, making debugging easier.

## Logging

The tool includes an advanced configurable logging system:

- Console logging with colored output for different log levels
- Optional file logging with automatic directory creation
- Configurable log formats and levels
- Convenience functions for creating specialized loggers
- Proper handler management to avoid duplicate log entries

By default, logs are printed to the console, but they can also be saved to a file using the `-l` option.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
