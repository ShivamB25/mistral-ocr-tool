"""API client for interacting with the Mistral OCR API."""
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union

from mistralai import Mistral

from config.settings import APIConfig
from utils.constants import OCRConstants
from utils.exceptions import APIError, ConfigurationError, FileError, UnsupportedFileTypeError
from utils.logger import logger

class MistralClient:
    """Client for interacting with the Mistral OCR API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Mistral client.
        
        Args:
            api_key: The Mistral API key. If None, it will be loaded from the environment.
            
        Raises:
            ConfigurationError: If the API key is not provided and not found in the environment.
        """
        self.api_key = api_key or APIConfig.MISTRAL_API_KEY
        
        if not self.api_key:
            raise ConfigurationError("Mistral API key not found. Please set the MISTRAL_API_KEY environment variable.")
        
        self.client = Mistral(api_key=self.api_key)
        logger.info("Mistral client initialized")
    
    def process_document(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Process a document using the Mistral OCR API.
        
        Args:
            file_path: The path to the document or a URL.
            
        Returns:
            The OCR response.
            
        Raises:
            UnsupportedFileTypeError: If the file type is not supported.
            FileError: If there is an error reading the file.
            APIError: If there is an error calling the API.
        """
        file_path_str = str(file_path)
        
        try:
            # Determine if the document is a local file or a URL
            if OCRConstants.is_url(file_path_str):
                logger.info(f"Processing URL: {file_path_str}")
                document = {
                    "type": OCRConstants.DOCUMENT_TYPES["url"], 
                    "document_url": file_path_str
                }
                
                ocr_response = self.client.ocr.process(
                    model=APIConfig.OCR_MODEL,
                    document=document,
                    include_image_base64=APIConfig.INCLUDE_IMAGES
                )
                
                logger.info(f"Successfully processed URL: {file_path_str}")
                return ocr_response
            else:
                # Check if the file type is supported
                if not OCRConstants.is_supported_file(file_path_str):
                    raise UnsupportedFileTypeError(file_path_str)
                
                logger.info(f"Processing file: {file_path_str}")
                
                # Upload the local file
                try:
                    with open(file_path_str, "rb") as f:
                        uploaded_file = self.client.files.upload(
                            file={
                                "file_name": os.path.basename(file_path_str), 
                                "content": f
                            },
                            purpose=OCRConstants.OCR_PURPOSE
                        )
                except FileNotFoundError:
                    raise FileError(f"File not found: {file_path_str}", file_path_str)
                except PermissionError:
                    raise FileError(f"Permission denied: {file_path_str}", file_path_str)
                except Exception as e:
                    raise FileError(f"Error reading file: {str(e)}", file_path_str)
                
                # Process the uploaded file
                ocr_response = self.client.ocr.process(
                    model=APIConfig.OCR_MODEL,
                    document={
                        "type": OCRConstants.DOCUMENT_TYPES["file_id"], 
                        "file_id": uploaded_file.id
                    },
                    include_image_base64=APIConfig.INCLUDE_IMAGES
                )
                
                logger.info(f"Successfully processed file: {file_path_str}")
                return ocr_response
                
        except (UnsupportedFileTypeError, FileError) as e:
            # Re-raise these exceptions as they are already properly formatted
            logger.error(str(e))
            raise
        except Exception as e:
            if "Mistral API" in str(e):
                logger.error(f"Mistral API error: {str(e)}")
                raise APIError(f"Mistral API error: {str(e)}")
            else:
                logger.error(f"Unexpected error processing document {file_path_str}: {str(e)}")
                raise APIError(f"Unexpected error: {str(e)}")
