"""
FastAPI application for the OCR API.

This module defines the FastAPI application and routes for the OCR API.
"""
import os
from typing import Optional
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from api.models import (
    OCRRequest, 
    OCRResponse, 
    OCRBatchRequest, 
    OCRBatchResponse,
    ProcessType,
    HealthResponse
)
from ocr.ocr_service import OCRService
from utils.api_client import MistralClient
from utils.exceptions import OCRToolError, InvalidInputError, APIError
from utils.logger import setup_logger


# Configure logging
logger = setup_logger(name="ocr_api")

# Create FastAPI app
app = FastAPI(
    title="Mistral OCR API",
    description="API for processing documents using the Mistral OCR API",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def get_ocr_service():
    """
    Dependency for getting an OCR service instance.
    
    Returns:
        OCRService: An initialized OCR service.
    """
    try:
        client = MistralClient()
        return OCRService(client)
    except OCRToolError as e:
        logger.error(f"Error initializing OCR service: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service health information.
    """
    return HealthResponse(
        status="healthy",
        version="0.1.0"
    )


@app.post("/ocr/process", response_model=OCRResponse)
async def process_document(
    request: OCRRequest,
    file: Optional[UploadFile] = File(None),
    ocr_service: OCRService = Depends(get_ocr_service)
):
    """
    Process a document using OCR.
    
    Args:
        request: The OCR request parameters.
        file: The file to process (for file uploads).
        ocr_service: The OCR service dependency.
        
    Returns:
        OCRResponse: The OCR processing results.
    """
    try:
        # Validate request
        if request.process_type == ProcessType.URL and not request.url:
            raise HTTPException(
                status_code=400, 
                detail="URL is required for URL processing"
            )
        
        if request.process_type == ProcessType.FILE and not file:
            raise HTTPException(
                status_code=400, 
                detail="File is required for file processing"
            )
        
        # Process based on type
        if request.process_type == ProcessType.URL:
            # Process URL
            logger.info(f"Processing URL: {request.url}")
            ocr_responses = ocr_service.process_documents(str(request.url))
            
            if not ocr_responses:
                raise HTTPException(
                    status_code=500, 
                    detail="Failed to process URL"
                )
                
            return ocr_responses[0]
        else:
            # Process file upload
            logger.info(f"Processing uploaded file: {file.filename}")
            
            # Save uploaded file to temporary file
            with NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
                temp_file_path = temp_file.name
                content = await file.read()
                temp_file.write(content)
            
            try:
                # Process the temporary file
                ocr_responses = ocr_service.process_documents(temp_file_path)
                
                if not ocr_responses:
                    raise HTTPException(
                        status_code=500, 
                        detail="Failed to process file"
                    )
                    
                return ocr_responses[0]
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
    except InvalidInputError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except OCRToolError as e:
        logger.error(f"OCR tool error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/ocr/batch", response_model=OCRBatchResponse)
async def process_batch(
    request: OCRBatchRequest,
    background_tasks: BackgroundTasks,
    ocr_service: OCRService = Depends(get_ocr_service)
):
    """
    Process multiple documents in batch mode.
    
    Args:
        request: The batch OCR request parameters.
        background_tasks: FastAPI background tasks.
        ocr_service: The OCR service dependency.
        
    Returns:
        OCRBatchResponse: The batch processing results.
    """
    results = []
    failed_urls = []
    
    for url in request.urls:
        try:
            logger.info(f"Processing URL in batch: {url}")
            ocr_responses = ocr_service.process_documents(str(url))
            
            if ocr_responses:
                results.append(ocr_responses[0])
            else:
                failed_urls.append(str(url))
                
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}")
            failed_urls.append(str(url))
    
    return OCRBatchResponse(
        results=results,
        failed_urls=failed_urls
    )
