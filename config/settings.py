"""Configuration settings for the OCR tool."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# API settings
class APIConfig:
    """API configuration settings."""
    
    MISTRAL_API_KEY: Optional[str] = os.environ.get("MISTRAL_API_KEY")
    OCR_MODEL: str = "mistral-ocr-latest"
    INCLUDE_IMAGES: bool = True

# File settings
class FileConfig:
    """File configuration settings."""
    
    DEFAULT_OUTPUT_DIR: Path = BASE_DIR / "output"
    
    @classmethod
    def ensure_output_dir(cls) -> None:
        """Ensure the output directory exists."""
        os.makedirs(cls.DEFAULT_OUTPUT_DIR, exist_ok=True)

# Create output directory if it doesn't exist
FileConfig.ensure_output_dir()
