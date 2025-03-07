"""
Server script for running the OCR API.

This module provides a command-line interface for running the OCR API
using Uvicorn.
"""
import argparse
import logging
import sys
from pathlib import Path

import uvicorn

from utils.logger import setup_logger


def parse_arguments():
    """
    Parse command-line arguments for the API server.
    
    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run the OCR API server.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--host", 
        default="0.0.0.0", 
        help="Host to bind the server to."
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="Port to bind the server to."
    )
    
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development."
    )
    
    parser.add_argument(
        "--workers", 
        type=int, 
        default=1, 
        help="Number of worker processes."
    )
    
    parser.add_argument(
        "--log-level", 
        choices=["debug", "info", "warning", "error", "critical"],
        default="info", 
        help="Logging level."
    )
    
    parser.add_argument(
        "--log-file", 
        help="Path to the log file."
    )
    
    return parser.parse_args()


def main():
    """
    Main function to run the OCR API server.
    
    Returns:
        int: 0 for success, 1 for failure.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Configure logging
    log_level_name = args.log_level.upper()
    log_level = getattr(logging, log_level_name)
    log_file = Path(args.log_file) if args.log_file else None
    logger = setup_logger(name="ocr_api_server", level=log_level, log_file=log_file)
    
    try:
        logger.info(f"Starting OCR API server on {args.host}:{args.port}")
        
        # Run the server
        uvicorn.run(
            "api.app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
            log_level=args.log_level.lower()
        )
        
        return 0
        
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
