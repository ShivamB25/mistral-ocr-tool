"""
Constants used throughout the OCR tool.

This module defines enums and constants used by the OCR tool,
including document types, file extensions, and utility methods.
"""
from enum import Enum
from typing import Dict, List


class DocumentType(Enum):
    """
    Document type enumeration for API requests.
    
    These values are used when making API requests to specify
    the type of document being processed.
    """
    URL = "document_url"
    FILE_ID = "file_id"


class OCRConstants:
    """
    OCR-related constants and utility methods.
    
    This class provides constants and utility methods for working
    with OCR documents, including document types, supported file
    extensions, and URL validation.
    """
    
    # Document types mapping
    DOCUMENT_TYPES: Dict[str, str] = {
        "url": DocumentType.URL.value,
        "file_id": DocumentType.FILE_ID.value
    }
    
    # OCR purpose identifier for API requests
    OCR_PURPOSE: str = "ocr"
    
    # URL prefixes for URL validation
    URL_PREFIXES: List[str] = ["http://", "https://"]
    
    # File extensions that can be processed by the OCR system
    SUPPORTED_EXTENSIONS: List[str] = [
        ".pdf",  # PDF documents
        ".png",  # PNG images
        ".jpg", ".jpeg",  # JPEG images
        ".tiff", ".tif",  # TIFF images
        ".bmp"  # Bitmap images
    ]
    
    @classmethod
    def is_url(cls, path: str) -> bool:
        """
        Check if a path is a URL.
        
        Args:
            path: The path to check.
            
        Returns:
            True if the path starts with a URL prefix, False otherwise.
        """
        return any(path.startswith(prefix) for prefix in cls.URL_PREFIXES)
    
    @classmethod
    def is_supported_file(cls, path: str) -> bool:
        """
        Check if a file has a supported extension.
        
        Args:
            path: The file path to check.
            
        Returns:
            True if the file has a supported extension, False otherwise.
        """
        return any(path.lower().endswith(ext) for ext in cls.SUPPORTED_EXTENSIONS)
