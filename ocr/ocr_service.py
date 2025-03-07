"""OCR service for processing documents using Optical Character Recognition."""
import os
from pathlib import Path
from typing import Dict, List, Any, Union

from utils.constants import OCRConstants
from utils.exceptions import InvalidInputError, OCRToolError
from utils.logger import logger
from utils.api_client import MistralClient


class OCRService:
    """
    Service for processing documents using OCR technology.
    
    This service handles different types of inputs (files, directories, URLs)
    and processes them using the Mistral OCR API.
    """
    
    def __init__(self, client: MistralClient):
        """
        Initialize the OCR service with a Mistral API client.
        
        Args:
            client: The Mistral API client for making OCR requests.
        """
        self.client = client
        logger.info("OCR service initialized")
    
    def process_documents(self, input_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Process multiple documents from a file, directory, or URL.
        
        This is the main entry point for document processing. It determines the
        type of input and delegates to the appropriate processing method.
        
        Args:
            input_path: The path to the input file or directory, or a URL.
            
        Returns:
            A list of dictionaries containing OCR responses.
            
        Raises:
            InvalidInputError: If the input path is invalid.
            OCRToolError: If there is an error processing the documents.
        """
        input_path_str = str(input_path)
        ocr_responses = []
        
        try:
            if OCRConstants.is_url(input_path_str):
                ocr_responses = self._process_url(input_path_str)
            elif os.path.isfile(input_path_str):
                ocr_responses = self._process_file(input_path_str)
            elif os.path.isdir(input_path_str):
                ocr_responses = self._process_directory(input_path_str)
            else:
                error_msg = f"Invalid input path: {input_path_str}. Must be a file, directory, or URL."
                logger.error(error_msg)
                raise InvalidInputError(error_msg)
                
            return ocr_responses
            
        except OCRToolError:
            # Re-raise OCRToolError exceptions
            raise
        except Exception as e:
            error_msg = f"Unexpected error processing documents: {str(e)}"
            logger.error(error_msg)
            raise OCRToolError(error_msg)
    
    def _process_url(self, url: str) -> List[Dict[str, Any]]:
        """
        Process a single URL using OCR.
        
        Args:
            url: The URL to process.
            
        Returns:
            A list containing a single OCR response.
        """
        logger.info(f"Processing URL: {url}")
        ocr_response = self.client.process_document(url)
        return [{"file": url, "response": ocr_response}]
    
    def _process_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a single file using OCR.
        
        Args:
            file_path: The path to the file to process.
            
        Returns:
            A list containing a single OCR response.
        """
        logger.info(f"Processing file: {file_path}")
        ocr_response = self.client.process_document(file_path)
        return [{"file": file_path, "response": ocr_response}]
    
    def _process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Process all supported files in a directory using OCR.
        
        Args:
            directory_path: The path to the directory to process.
            
        Returns:
            A list of OCR responses, one for each successfully processed file.
        """
        logger.info(f"Processing directory: {directory_path}")
        ocr_responses = []
        
        # Get all files in the directory
        files = self._get_files_in_directory(directory_path)
        
        # Filter for supported file types
        supported_files = self._filter_supported_files(files)
        
        if not supported_files:
            logger.warning(f"No supported files found in directory: {directory_path}")
            return ocr_responses
        
        # Process each file
        for file_path in supported_files:
            try:
                logger.info(f"Processing file: {file_path}")
                ocr_response = self.client.process_document(file_path)
                ocr_responses.append({
                    "file": os.path.basename(file_path), 
                    "response": ocr_response
                })
            except OCRToolError as e:
                # Log the error but continue processing other files
                logger.error(f"Error processing file {file_path}: {str(e)}")
                continue
        
        return ocr_responses
    
    @staticmethod
    def _get_files_in_directory(directory_path: str) -> List[str]:
        """
        Get all files in a directory.
        
        Args:
            directory_path: The path to the directory.
            
        Returns:
            A list of file paths.
        """
        return [
            os.path.join(directory_path, f) 
            for f in os.listdir(directory_path) 
            if os.path.isfile(os.path.join(directory_path, f))
        ]
    
    @staticmethod
    def _filter_supported_files(files: List[str]) -> List[str]:
        """
        Filter a list of files to include only supported file types.
        
        Args:
            files: A list of file paths.
            
        Returns:
            A list of supported file paths.
        """
        return [
            f for f in files 
            if OCRConstants.is_supported_file(f)
        ]
