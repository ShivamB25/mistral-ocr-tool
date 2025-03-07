#!/usr/bin/env python3
"""
Mistral OCR Tool - Process documents using the Mistral OCR API.

This tool can process a single file, a directory of files, or a URL.
It extracts text and other information from documents using OCR technology.

The tool can be run in two modes:
1. CLI mode: Process documents from the command line
2. API mode: Run as a REST API server using FastAPI and Uvicorn
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from ocr.ocr_service import OCRService
from utils.api_client import MistralClient
from utils.file_handler import FileHandler
from utils.exceptions import OCRToolError
from utils.logger import setup_logger


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser for CLI mode.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Process documents using the Mistral OCR API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Add subparsers for different modes
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")
    
    # CLI mode parser
    cli_parser = subparsers.add_parser(
        "cli", 
        help="Run in CLI mode to process documents from the command line"
    )
    
    cli_parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Path to the input file or directory, or a URL."
    )
    
    cli_parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Path to the output file."
    )
    
    cli_parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose logging."
    )
    
    cli_parser.add_argument(
        "-l", "--log-file", 
        help="Path to the log file."
    )
    
    # API mode parser
    api_parser = subparsers.add_parser(
        "api", 
        help="Run in API mode as a REST API server"
    )
    
    api_parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind the server to."
    )
    
    api_parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to."
    )
    
    api_parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development."
    )
    
    api_parser.add_argument(
        "--workers", 
        type=int, 
        default=1, 
        help="Number of worker processes."
    )
    
    api_parser.add_argument(
        "--log-level", 
        choices=["debug", "info", "warning", "error", "critical"],
        default="info", 
        help="Logging level."
    )
    
    api_parser.add_argument(
        "--log-file", 
        help="Path to the log file."
    )
    
    return parser


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Default to CLI mode if no mode specified
    if args.mode is None:
        parser.print_help()
        sys.exit(1)
        
    return args


def configure_logging(verbose: bool, log_file_path: Optional[str]) -> logging.Logger:
    """
    Configure the logging system for CLI mode.
    
    Args:
        verbose: Whether to enable verbose (DEBUG) logging.
        log_file_path: Optional path to a log file.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    log_file = Path(log_file_path) if log_file_path else None
    return setup_logger(level=log_level, log_file=log_file)


def process_documents(input_path: str, logger: logging.Logger) -> List[Dict[str, Any]]:
    """
    Process documents using OCR.
    
    Args:
        input_path: Path to the input file, directory, or URL.
        logger: Logger instance for logging.
        
    Returns:
        List[Dict[str, Any]]: List of OCR responses.
        
    Raises:
        OCRToolError: If there is an error processing the documents.
    """
    # Initialize the Mistral client
    client = MistralClient()
    
    # Initialize the OCR service
    ocr_service = OCRService(client)
    
    # Process the documents
    logger.info(f"Processing input: {input_path}")
    return ocr_service.process_documents(input_path)


def save_results(ocr_responses: List[Dict[str, Any]], output_path: str, logger: logging.Logger) -> None:
    """
    Save OCR results to the specified output file.
    
    Args:
        ocr_responses: List of OCR responses.
        output_path: Path to the output file.
        logger: Logger instance for logging.
        
    Raises:
        OCRToolError: If there is an error saving the results.
    """
    logger.info(f"Saving output to: {output_path}")
    FileHandler.save_output(ocr_responses, output_path)
    logger.info("Processing completed successfully")


def run_cli_mode(args: argparse.Namespace) -> int:
    """
    Run the OCR tool in CLI mode.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: 0 for success, 1 for failure.
    """
    # Configure logging
    logger = configure_logging(args.verbose, args.log_file)
    
    try:
        # Process documents
        ocr_responses = process_documents(args.input, logger)
        
        # Save results
        save_results(ocr_responses, args.output, logger)
        
        return 0
        
    except OCRToolError as e:
        logger.error(f"Error: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1


def run_api_mode(args: argparse.Namespace) -> int:
    """
    Run the OCR tool in API mode.
    
    Args:
        args: Command-line arguments.
        
    Returns:
        int: 0 for success, 1 for failure.
    """
    try:
        # Import here to avoid circular imports
        from api.server import main as run_server
        
        # Run the API server
        return run_server()
        
    except ImportError:
        print("Error: API dependencies not installed. Please install with:")
        print("uv pip install -e '.[api]'")
        return 1
    except Exception as e:
        print(f"Error starting API server: {str(e)}")
        return 1


def main() -> int:
    """
    Main entry point for the OCR tool.
    
    Returns:
        int: 0 for success, 1 for failure.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Run in the appropriate mode
    if args.mode == "cli":
        return run_cli_mode(args)
    elif args.mode == "api":
        return run_api_mode(args)
    else:
        print(f"Error: Unknown mode '{args.mode}'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
