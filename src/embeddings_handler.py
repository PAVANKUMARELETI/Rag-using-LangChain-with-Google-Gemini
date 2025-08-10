"""
Embeddings handler for creating and managing vector embeddings.
"""
import os
import logging
from typing import List, Optional, Any

# Try different import paths for LangChain components
try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
except ImportError:
    GoogleGenerativeAIEmbeddings = None

try:
    from langchain_community.vectorstores import Chroma
except ImportError:
    try:
        from langchain.vectorstores import Chroma
    except ImportError:
        Chroma = None

from .config import Config

logger = logging.getLogger(__name__)

class EmbeddingsHandler:
    """Handler for creating and managing document embeddings."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        embedding_model: Optional[str] = None,
        vector_db_path: Optional[str] = None
    ):
        """
        Initialize the embeddings handler.
        
        Args:
            api_key: Google AI API key. If None, uses Config.GOOGLE_API_KEY
            embedding_model: Embedding model name. If None, uses Config.EMBEDDING_MODEL
            vector_db_path: Path for vector database. If None, uses Config.VECTOR_DB_PATH
        """
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.embedding_model = embedding_model or Config.EMBEDDING_MODEL
        self.vector_db_path = vector_db_path or Config.VECTOR_DB_PATH
        
        if not self.api_key:
            raise ValueError("Google AI API key is required")
        
        # Initialize embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=self.embedding_model,
            google_api_key=self.api_key
        )
        
        # Vector store will be initialized when needed
        self.vector_store = None
        
        logger.info(f"Initialized EmbeddingsHandler with model: {self.embedding_model}")
    
    def create_vector_store(self, texts: List[str]) -> Chroma:
        """
        Create a vector store from text chunks.
        
        Args:
            texts: List of text chunks to embed
            
        Returns:
            Chroma vector store
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.vector_db_path), exist_ok=True)
            
            # Create vector store
            self.vector_store = Chroma.from_texts(
                texts=texts,
                embedding=self.embeddings,
                persist_directory=self.vector_db_path
            )
            
            logger.info(f"Created vector store with {len(texts)} documents")
            return self.vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise
    
    def load_vector_store(self) -> Optional[Chroma]:
        """
        Load existing vector store from disk.
        
        Returns:
            Chroma vector store if exists, None otherwise
        """
        try:
            if os.path.exists(self.vector_db_path):
                self.vector_store = Chroma(
                    persist_directory=self.vector_db_path,
                    embedding_function=self.embeddings
                )
                logger.info(f"Loaded existing vector store from {self.vector_db_path}")
                return self.vector_store
            else:
                logger.warning(f"Vector store not found at {self.vector_db_path}")
                return None
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            raise
    
    def add_texts(self, texts: List[str]) -> None:
        """
        Add new texts to existing vector store.
        
        Args:
            texts: List of text chunks to add
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call create_vector_store first.")
        
        try:
            self.vector_store.add_texts(texts)
            logger.info(f"Added {len(texts)} new documents to vector store")
        except Exception as e:
            logger.error(f"Error adding texts to vector store: {str(e)}")
            raise
    
    def similarity_search(
        self, 
        query: str, 
        k: Optional[int] = None
    ) -> List[Any]:
        """
        Perform similarity search in the vector store.
        
        Args:
            query: Query text
            k: Number of similar documents to return
            
        Returns:
            List of similar documents
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        k = k or Config.SIMILARITY_SEARCH_K
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            raise
    
    def get_retriever(self, search_kwargs: Optional[dict] = None) -> Any:
        """
        Get a retriever from the vector store.
        
        Args:
            search_kwargs: Search parameters
            
        Returns:
            Retriever object
        """
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        search_kwargs = search_kwargs or {"k": Config.SIMILARITY_SEARCH_K}
        
        try:
            retriever = self.vector_store.as_retriever(search_kwargs=search_kwargs)
            logger.info("Created retriever from vector store")
            return retriever
        except Exception as e:
            logger.error(f"Error creating retriever: {str(e)}")
            raise
    
    def persist_vector_store(self) -> None:
        """Persist the vector store to disk."""
        if not self.vector_store:
            raise ValueError("Vector store not initialized")
        
        try:
            self.vector_store.persist()
            logger.info(f"Persisted vector store to {self.vector_db_path}")
        except Exception as e:
            logger.error(f"Error persisting vector store: {str(e)}")
            raise
    
    def delete_vector_store(self) -> None:
        """Delete the vector store from disk."""
        try:
            if os.path.exists(self.vector_db_path):
                import shutil
                shutil.rmtree(self.vector_db_path)
                logger.info(f"Deleted vector store at {self.vector_db_path}")
            self.vector_store = None
        except Exception as e:
            logger.error(f"Error deleting vector store: {str(e)}")
            raise
    
    def get_vector_store_info(self) -> dict:
        """
        Get information about the current vector store.
        
        Returns:
            Dictionary with vector store information
        """
        if not self.vector_store:
            return {"status": "not_initialized"}
        
        try:
            # Get collection info
            collection = self.vector_store._collection
            return {
                "status": "initialized",
                "count": collection.count(),
                "path": self.vector_db_path,
                "embedding_model": self.embedding_model
            }
        except Exception as e:
            logger.error(f"Error getting vector store info: {str(e)}")
            return {"status": "error", "error": str(e)}
