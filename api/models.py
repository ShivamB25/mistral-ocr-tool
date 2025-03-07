"""
API data models for the OCR API.

This module defines Pydantic models for request and response data
used in the FastAPI application.
"""
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, HttpUrl


class ProcessType(str, Enum):
    """Type of document processing."""
    
    URL = "url"
    FILE = "file"


class OCRRequest(BaseModel):
    """
    Request model for OCR processing.
    
    This model is used for both URL and file upload processing.
    For file uploads, the 'url' field is ignored and the file
    is uploaded using FastAPI's File handling.
    """
    
    process_type: ProcessType = Field(
        ..., 
        description="Type of processing (url or file)"
    )
    url: Optional[HttpUrl] = Field(
        None, 
        description="URL of the document to process (required for URL processing)"
    )
    include_images: bool = Field(
        False, 
        description="Whether to include base64-encoded images in the response"
    )


class OCRResponse(BaseModel):
    """Response model for OCR processing."""
    
    file: str = Field(..., description="Filename or URL that was processed")
    response: Dict[str, Any] = Field(..., description="OCR response data")


class OCRBatchRequest(BaseModel):
    """Request model for batch OCR processing."""
    
    urls: List[HttpUrl] = Field(
        ..., 
        description="List of URLs to process",
        min_items=1,
        max_items=10
    )
    include_images: bool = Field(
        False, 
        description="Whether to include base64-encoded images in the response"
    )


class OCRBatchResponse(BaseModel):
    """Response model for batch OCR processing."""
    
    results: List[OCRResponse] = Field(..., description="List of OCR responses")
    failed_urls: List[str] = Field(
        default_factory=list, 
        description="List of URLs that failed to process"
    )


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
