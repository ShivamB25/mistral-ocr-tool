"""
File handling utilities for the OCR tool.

This module provides utilities for file operations, including
saving OCR responses to JSON files and handling file-related errors.
"""
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Any, Union, Iterator

from utils.exceptions import FileError
from utils.logger import logger


class FileHandler:
    """
    File handling utilities for the OCR tool.
    
    This class provides static methods for common file operations
    used throughout the OCR tool.
    """
    
    @staticmethod
    def save_output(ocr_responses: List[Dict[str, Any]], output_path: Union[str, Path]) -> None:
        """
        Save OCR responses to a JSON file.
        
        This method converts OCR response objects to dictionaries and
        saves them to a JSON file at the specified path. It creates
        any necessary directories in the path if they don't exist.
        
        Args:
            ocr_responses: A list of dictionaries containing OCR responses.
            output_path: The path to save the output file.
            
        Raises:
            FileError: If there is an error saving the file.
        """
        # Convert to Path object for better path handling
        path = Path(output_path)
        
        try:
            # Create the directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert OCRResponse objects to dictionaries
            ocr_responses_dict = [
                {
                    "file": item["file"], 
                    "response": item["response"].model_dump()
                }
                for item in ocr_responses
            ]
            
            # Write to file using a context manager
            with path.open("w") as f:
                json.dump(ocr_responses_dict, f, indent=4)
                
            logger.info(f"OCR responses saved to {path}")
            
        except PermissionError:
            error_msg = f"Permission denied: {path}"
            logger.error(error_msg)
            raise FileError(error_msg, str(path))
        except IsADirectoryError:
            error_msg = f"Is a directory: {path}"
            logger.error(error_msg)
            raise FileError(error_msg, str(path))
        except Exception as e:
            error_msg = f"Error saving output: {str(e)}"
            logger.error(f"{error_msg} to {path}")
            raise FileError(error_msg, str(path))
    
    @staticmethod
    @contextmanager
    def safe_open(file_path: Union[str, Path], mode: str = "r") -> Iterator[Any]:
        """
        Safely open a file with proper error handling.
        
        This context manager provides a safe way to open files with
        appropriate error handling and conversion to FileError exceptions.
        
        Args:
            file_path: The path to the file to open.
            mode: The file open mode (e.g., "r", "w", "rb").
            
        Yields:
            The opened file object.
            
        Raises:
            FileError: If there is an error opening the file.
        """
        path = Path(file_path)
        
        try:
            # Create parent directories if writing
            if "w" in mode:
                path.parent.mkdir(parents=True, exist_ok=True)
                
            file = path.open(mode)
            try:
                yield file
            finally:
                file.close()
        except FileNotFoundError:
            error_msg = f"File not found: {path}"
            logger.error(error_msg)
            raise FileError(error_msg, str(path))
        except PermissionError:
            error_msg = f"Permission denied: {path}"
            logger.error(error_msg)
            raise FileError(error_msg, str(path))
        except IsADirectoryError:
            error_msg = f"Is a directory: {path}"
            logger.error(error_msg)
            raise FileError(error_msg, str(path))
        except Exception as e:
            error_msg = f"Error accessing file: {str(e)}"
            logger.error(f"{error_msg} - {path}")
            raise FileError(error_msg, str(path))
