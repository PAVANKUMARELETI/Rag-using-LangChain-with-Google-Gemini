"""
Demo script to showcase RAG functionality.
"""
import os
import sys
import logging
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent
sys.path.append(str(src_path))

from config import Config
from rag_chain import RAGChain

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main demo function."""
    print("🚀 RAG using LangChain with Google Gemini Demo")
    print("=" * 50)
    
    try:
        # Initialize RAG system
        print("Initializing RAG system...")
        rag = RAGChain()
        
        # Load sample document
        sample_url = "http://jmc.stanford.edu/articles/whatisai/whatisai.pdf"
        print(f"Loading document: {sample_url}")
        
        num_chunks = rag.load_documents_from_url(sample_url)
        print(f"✅ Loaded and processed {num_chunks} text chunks")
        
        # Ask sample questions
        questions = [
            "What is artificial intelligence?",
            "Who can learn AI?",
            "What are the main applications of AI?",
            "How does machine learning relate to AI?"
        ]
        
        print("\n🤔 Asking sample questions:")
        print("-" * 30)
        
        for i, question in enumerate(questions, 1):
            print(f"\nQ{i}: {question}")
            answer = rag.chat(question)
            print(f"A{i}: {answer}")
            print("-" * 30)
        
        print("\n✅ Demo completed successfully!")
        print("You can now use the RAG system in your Jupyter notebook.")
        
    except Exception as e:
        print(f"❌ Error running demo: {str(e)}")
        print("Make sure you have set up your Google AI API key in the .env file")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
