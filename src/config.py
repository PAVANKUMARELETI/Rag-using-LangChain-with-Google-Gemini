"""
Configuration management for the RAG application.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for RAG application settings."""
    
    # Google AI Settings
    GOOGLE_API_KEY: Optional[str] = os.getenv('GOOGLE_API_KEY')
    GEMINI_MODEL: str = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash-latest')
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'models/embedding-001')
    
    # Text Processing Settings
    CHUNK_SIZE: int = int(os.getenv('CHUNK_SIZE', '700'))
    CHUNK_OVERLAP: int = int(os.getenv('CHUNK_OVERLAP', '100'))
    
    # Vector Store Settings
    VECTOR_DB_PATH: str = os.getenv('VECTOR_DB_PATH', './vector_db')
    SIMILARITY_SEARCH_K: int = int(os.getenv('SIMILARITY_SEARCH_K', '5'))
    
    # Model Parameters
    DEFAULT_TEMPERATURE: float = float(os.getenv('DEFAULT_TEMPERATURE', '0.8'))
    DEFAULT_MAX_OUTPUT_TOKENS: int = int(os.getenv('DEFAULT_MAX_OUTPUT_TOKENS', '1024'))
    DEFAULT_TOP_K: int = int(os.getenv('DEFAULT_TOP_K', '32'))
    DEFAULT_TOP_P: float = float(os.getenv('DEFAULT_TOP_P', '1.0'))
    
    # File Paths
    DATA_DIR: str = os.getenv('DATA_DIR', './data')
    DOCUMENTS_DIR: str = os.getenv('DOCUMENTS_DIR', './data/documents')
    OUTPUTS_DIR: str = os.getenv('OUTPUTS_DIR', './outputs')
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration parameters."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required but not set")
        return True
    
    @classmethod
    def get_generation_config(cls, **kwargs) -> dict:
        """Get generation configuration with optional overrides."""
        config = {
            'temperature': kwargs.get('temperature', cls.DEFAULT_TEMPERATURE),
            'max_output_tokens': kwargs.get('max_output_tokens', cls.DEFAULT_MAX_OUTPUT_TOKENS),
            'top_k': kwargs.get('top_k', cls.DEFAULT_TOP_K),
            'top_p': kwargs.get('top_p', cls.DEFAULT_TOP_P),
        }
        return {k: v for k, v in config.items() if v is not None}
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist."""
        directories = [
            cls.DATA_DIR,
            cls.DOCUMENTS_DIR, 
            cls.OUTPUTS_DIR,
            cls.VECTOR_DB_PATH
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
