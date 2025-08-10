"""
Document processing utilities for PDF loading and text splitting.
"""
import os
import logging
from typing import List, Optional

# Try different import paths for LangChain components
try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    try:
        from langchain.document_loaders import PyPDFLoader
    except ImportError:
        PyPDFLoader = None

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        RecursiveCharacterTextSplitter = None

try:
    from langchain.schema import Document
except ImportError:
    try:
        from langchain_core.documents import Document
    except ImportError:
        Document = None

from .config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Document processing class for PDF loading and text splitting."""
    
    def __init__(
        self, 
        chunk_size: Optional[int] = None, 
        chunk_overlap: Optional[int] = None
    ):
        """
        Initialize the document processor.
        
        Args:
            chunk_size: Size of text chunks. If None, uses Config.CHUNK_SIZE
            chunk_overlap: Overlap between chunks. If None, uses Config.CHUNK_OVERLAP
        """
        if not PyPDFLoader:
            raise ImportError("PyPDFLoader not available. Install with: pip install langchain-community")
        
        if not RecursiveCharacterTextSplitter:
            raise ImportError("RecursiveCharacterTextSplitter not available. Install with: pip install langchain-text-splitters")
        
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        
        logger.info(f"Initialized DocumentProcessor with chunk_size={self.chunk_size}, chunk_overlap={self.chunk_overlap}")
    
    def load_pdf_from_url(self, url: str) -> List:
        """
        Load PDF document from URL.
        
        Args:
            url: URL of the PDF document
            
        Returns:
            List of Document objects
        """
        try:
            loader = PyPDFLoader(url)
            documents = loader.load_and_split()
            logger.info(f"Loaded {len(documents)} pages from PDF: {url}")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF from URL {url}: {str(e)}")
            raise
    
    def load_pdf_from_file(self, file_path: str) -> List:
        """
        Load PDF document from local file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of Document objects
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load_and_split()
            logger.info(f"Loaded {len(documents)} pages from PDF: {file_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF from file {file_path}: {str(e)}")
            raise
    
    def load_pdfs_from_directory(self, directory_path: str) -> List:
        """
        Load all PDF documents from a directory.
        
        Args:
            directory_path: Path to directory containing PDF files
            
        Returns:
            List of Document objects from all PDFs
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        all_documents = []
        pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            logger.warning(f"No PDF files found in directory: {directory_path}")
            return all_documents
        
        for pdf_file in pdf_files:
            file_path = os.path.join(directory_path, pdf_file)
            try:
                documents = self.load_pdf_from_file(file_path)
                all_documents.extend(documents)
            except Exception as e:
                logger.error(f"Error processing {pdf_file}: {str(e)}")
                continue
        
        logger.info(f"Loaded total {len(all_documents)} pages from {len(pdf_files)} PDF files")
        return all_documents
    
    def split_documents(self, documents: List) -> List[str]:
        """
        Split documents into chunks.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of text chunks
        """
        try:
            # Combine all document content
            context = "\n\n".join(doc.page_content for doc in documents)
            
            # Split into chunks
            chunks = self.text_splitter.split_text(context)
            
            logger.info(f"Split documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise
    
    def process_pdf_url(self, url: str) -> List[str]:
        """
        Complete processing pipeline for PDF from URL.
        
        Args:
            url: URL of the PDF document
            
        Returns:
            List of text chunks
        """
        documents = self.load_pdf_from_url(url)
        return self.split_documents(documents)
    
    def process_pdf_file(self, file_path: str) -> List[str]:
        """
        Complete processing pipeline for PDF from file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of text chunks
        """
        documents = self.load_pdf_from_file(file_path)
        return self.split_documents(documents)
    
    def process_pdf_directory(self, directory_path: str) -> List[str]:
        """
        Complete processing pipeline for all PDFs in directory.
        
        Args:
            directory_path: Path to directory containing PDF files
            
        Returns:
            List of text chunks from all PDFs
        """
        documents = self.load_pdfs_from_directory(directory_path)
        return self.split_documents(documents)
    
    def get_document_stats(self, documents: List) -> dict:
        """
        Get statistics about the loaded documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Dictionary with document statistics
        """
        if not documents:
            return {
                'total_pages': 0,
                'total_characters': 0,
                'average_page_length': 0
            }
        
        total_chars = sum(len(doc.page_content) for doc in documents)
        
        return {
            'total_pages': len(documents),
            'total_characters': total_chars,
            'average_page_length': total_chars / len(documents) if documents else 0
        }
