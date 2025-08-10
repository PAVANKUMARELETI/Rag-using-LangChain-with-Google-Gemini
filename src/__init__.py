# RAG using LangChain with Google Gemini
# Source code modules for the RAG application

__version__ = "1.0.0"
__author__ = "RAG Project Team"
__email__ = "contact@ragproject.com"

from .config import Config
from .gemini_client import GeminiClient
from .document_processor import DocumentProcessor
from .embeddings_handler import EmbeddingsHandler
from .rag_chain import RAGChain

__all__ = [
    "Config",
    "GeminiClient", 
    "DocumentProcessor",
    "EmbeddingsHandler",
    "RAGChain"
]
