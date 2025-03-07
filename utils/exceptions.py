"""
Custom exceptions for the OCR tool.

This module defines a hierarchy of custom exceptions used throughout
the OCR tool to provide clear error messages and proper error handling.
"""
from typing import Optional


class OCRToolError(Exception):
    """
    Base exception for all OCR tool errors.
    
    This is the parent class for all custom exceptions in the OCR tool.
    It provides a common interface and behavior for all derived exceptions.
    """
    
    def __init__(self, message: str = "An error occurred in the OCR tool"):
        """
        Initialize the base OCR tool exception.
        
        Args:
            message: A descriptive error message.
        """
        self.message = message
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """
        Return a string representation of the exception.
        
        Returns:
            The error message.
        """
        return self.message


class APIError(OCRToolError):
    """
    Exception raised for API-related errors.
    
    This exception is used when there are errors communicating with
    external APIs, such as the Mistral OCR API.
    """
    
    def __init__(self, message: str = "API error", status_code: Optional[int] = None):
        """
        Initialize an API error exception.
        
        Args:
            message: A descriptive error message.
            status_code: The HTTP status code associated with the error, if applicable.
        """
        self.status_code = status_code
        message_with_code = f"{message}" + (f" (Status code: {status_code})" if status_code else "")
        super().__init__(message_with_code)


class ConfigurationError(OCRToolError):
    """
    Exception raised for configuration-related errors.
    
    This exception is used when there are issues with the tool's
    configuration, such as missing API keys or invalid settings.
    """
    
    def __init__(self, message: str = "Configuration error"):
        """
        Initialize a configuration error exception.
        
        Args:
            message: A descriptive error message.
        """
        super().__init__(message)


class FileError(OCRToolError):
    """
    Exception raised for file-related errors.
    
    This exception is used when there are issues with file operations,
    such as file not found, permission denied, or I/O errors.
    """
    
    def __init__(self, message: str = "File error", file_path: Optional[str] = None):
        """
        Initialize a file error exception.
        
        Args:
            message: A descriptive error message.
            file_path: The path to the file that caused the error, if applicable.
        """
        self.file_path = file_path
        message_with_path = f"{message}" + (f" (Path: {file_path})" if file_path else "")
        super().__init__(message_with_path)


class UnsupportedFileTypeError(FileError):
    """
    Exception raised when a file type is not supported.
    
    This exception is used when attempting to process a file with
    an unsupported extension or format.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize an unsupported file type error exception.
        
        Args:
            file_path: The path to the unsupported file, if applicable.
        """
        super().__init__("Unsupported file type", file_path)


class InvalidInputError(OCRToolError):
    """
    Exception raised for invalid input.
    
    This exception is used when the input provided to a function
    or method is invalid or does not meet the expected format.
    """
    
    def __init__(self, message: str = "Invalid input"):
        """
        Initialize an invalid input error exception.
        
        Args:
            message: A descriptive error message.
        """
        super().__init__(message)
