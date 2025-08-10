"""
RAG (Retrieval-Augmented Generation) chain implementation.
"""
import logging
from typing import Optional, Dict, Any, List

# Try different import paths for LangChain components
try:
    from langchain.chains import RetrievalQA
except ImportError:
    try:
        from langchain_community.chains import RetrievalQA
    except ImportError:
        RetrievalQA = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

from .config import Config
from .gemini_client import GeminiClient
from .document_processor import DocumentProcessor
from .embeddings_handler import EmbeddingsHandler

logger = logging.getLogger(__name__)

class RAGChain:
    """Complete RAG chain implementation with document processing and Q&A."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None
    ):
        """
        Initialize the RAG chain.
        
        Args:
            api_key: Google AI API key
            model_name: Gemini model name
            temperature: Model temperature
        """
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.model_name = model_name or Config.GEMINI_MODEL
        self.temperature = temperature or Config.DEFAULT_TEMPERATURE
        
        if not self.api_key:
            raise ValueError("Google AI API key is required")
        
        # Initialize components
        self.gemini_client = GeminiClient(self.api_key, self.model_name)
        self.document_processor = DocumentProcessor()
        self.embeddings_handler = EmbeddingsHandler(self.api_key)
        
        # Initialize LangChain components
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=self.temperature
        )
        
        self.qa_chain = None
        self.retriever = None
        
        logger.info("Initialized RAG chain")
    
    def load_documents_from_url(self, url: str) -> int:
        """
        Load and process documents from URL.
        
        Args:
            url: URL of the PDF document
            
        Returns:
            Number of text chunks created
        """
        try:
            # Process document
            texts = self.document_processor.process_pdf_url(url)
            
            # Create vector store
            self.embeddings_handler.create_vector_store(texts)
            
            # Create retriever
            self.retriever = self.embeddings_handler.get_retriever()
            
            # Create QA chain
            self._create_qa_chain()
            
            logger.info(f"Loaded documents from URL: {url}")
            return len(texts)
        except Exception as e:
            logger.error(f"Error loading documents from URL: {str(e)}")
            raise
    
    def load_documents_from_file(self, file_path: str) -> int:
        """
        Load and process documents from file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Number of text chunks created
        """
        try:
            # Process document
            texts = self.document_processor.process_pdf_file(file_path)
            
            # Create vector store
            self.embeddings_handler.create_vector_store(texts)
            
            # Create retriever
            self.retriever = self.embeddings_handler.get_retriever()
            
            # Create QA chain
            self._create_qa_chain()
            
            logger.info(f"Loaded documents from file: {file_path}")
            return len(texts)
        except Exception as e:
            logger.error(f"Error loading documents from file: {str(e)}")
            raise
    
    def load_documents_from_directory(self, directory_path: str) -> int:
        """
        Load and process documents from directory.
        
        Args:
            directory_path: Path to directory containing PDF files
            
        Returns:
            Number of text chunks created
        """
        try:
            # Process documents
            texts = self.document_processor.process_pdf_directory(directory_path)
            
            if not texts:
                raise ValueError("No documents found to process")
            
            # Create vector store
            self.embeddings_handler.create_vector_store(texts)
            
            # Create retriever
            self.retriever = self.embeddings_handler.get_retriever()
            
            # Create QA chain
            self._create_qa_chain()
            
            logger.info(f"Loaded documents from directory: {directory_path}")
            return len(texts)
        except Exception as e:
            logger.error(f"Error loading documents from directory: {str(e)}")
            raise
    
    def _create_qa_chain(self) -> None:
        """Create the QA chain."""
        if not self.retriever:
            raise ValueError("Retriever not initialized")
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True
        )
        
        logger.info("Created QA chain")
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Ask a question using the RAG system.
        
        Args:
            question: Question to ask
            
        Returns:
            Dictionary with answer and source documents
        """
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Load documents first.")
        
        try:
            result = self.qa_chain.invoke({"query": question})
            
            logger.info(f"Processed query: {question}")
            
            return {
                "question": question,
                "answer": result["result"],
                "source_documents": result["source_documents"]
            }
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    def chat(self, question: str) -> str:
        """
        Simple chat interface that returns just the answer.
        
        Args:
            question: Question to ask
            
        Returns:
            Answer string
        """
        result = self.query(question)
        return result["answer"]
    
    def get_similar_documents(self, query: str, k: Optional[int] = None) -> List[Any]:
        """
        Get similar documents without generating an answer.
        
        Args:
            query: Query text
            k: Number of documents to return
            
        Returns:
            List of similar documents
        """
        if not self.embeddings_handler.vector_store:
            raise ValueError("Vector store not initialized. Load documents first.")
        
        return self.embeddings_handler.similarity_search(query, k)
    
    def update_temperature(self, temperature: float) -> None:
        """
        Update the model temperature.
        
        Args:
            temperature: New temperature value
        """
        self.temperature = temperature
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=self.api_key,
            temperature=self.temperature
        )
        
        # Recreate QA chain with new LLM
        if self.retriever:
            self._create_qa_chain()
        
        logger.info(f"Updated temperature to {temperature}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get information about the RAG system.
        
        Returns:
            Dictionary with system information
        """
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "vector_store_info": self.embeddings_handler.get_vector_store_info(),
            "qa_chain_ready": self.qa_chain is not None,
            "retriever_ready": self.retriever is not None
        }
    
    def reset(self) -> None:
        """Reset the RAG system by clearing all loaded data."""
        try:
            self.embeddings_handler.delete_vector_store()
            self.qa_chain = None
            self.retriever = None
            logger.info("Reset RAG system")
        except Exception as e:
            logger.error(f"Error resetting RAG system: {str(e)}")
            raise
