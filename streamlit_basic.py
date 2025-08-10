"""
🚀 RAG Basic - Simplified Streamlit App for Python 3.8
Works without advanced LangChain components.
"""

import streamlit as st
import sys
import os
import time
import requests
from pathlib import Path

# Try importing available packages
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    st.error("google.generativeai not available. Install with: pip install google-generativeai")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="RAG Basic with Gemini",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'genai_model' not in st.session_state:
    st.session_state.genai_model = None

def setup_genai(api_key):
    """Setup Google Generative AI with API key."""
    if not GENAI_AVAILABLE:
        return False, "Google Generative AI not available"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # Test the connection
        response = model.generate_content("Hello")
        st.session_state.genai_model = model
        st.session_state.api_key_set = True
        return True, "API key validated successfully!"
    except Exception as e:
        return False, f"Error setting up API: {str(e)}"

def simple_text_split(text, chunk_size=1000):
    """Simple text splitting function."""
    sentences = text.split('.')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk + sentence) < chunk_size:
            current_chunk += sentence + "."
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_text_from_url(url):
    """Simple text extraction from URL (for demonstration)."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Very basic text extraction
            text = response.text
            # Remove HTML tags (basic)
            import re
            text = re.sub(r'<[^>]+>', '', text)
            return text[:5000]  # Limit for demo
        else:
            return None
    except:
        return None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 RAG Basic with Gemini</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Simplified RAG System - Python 3.8 Compatible</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🛠️ Setup")
        
        # API Key input
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        
        if api_key and not st.session_state.api_key_set:
            if st.button("🔐 Setup API Key"):
                success, message = setup_genai(api_key)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        
        # System status
        st.markdown("### 📊 System Status")
        if GENAI_AVAILABLE:
            st.success("✅ Google AI: Available")
        else:
            st.error("❌ Google AI: Missing")
        
        if st.session_state.api_key_set:
            st.success("✅ API Key: Configured")
        else:
            st.error("❌ API Key: Not Set")
        
        if PLOTLY_AVAILABLE:
            st.success("✅ Charts: Available")
        else:
            st.warning("⚠️ Charts: Limited")
    
    # Main content
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set up your Google AI API key in the sidebar to begin.")
        
        st.markdown("## 🎯 What is RAG?")
        st.markdown("""
        **Retrieval-Augmented Generation (RAG)** combines:
        - 🔍 **Information Retrieval**: Finding relevant documents
        - 🤖 **Text Generation**: Creating responses using AI
        - 📚 **Knowledge Base**: Your own documents and data
        
        ### 🚀 Getting Started
        1. Enter your Google AI API key in the sidebar
        2. Upload or link to documents
        3. Start asking questions about your content
        """)
        
        return
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📄 Documents", "🧪 Experiments", "📊 Analytics"])
    
    with tab1:
        st.markdown("## 💬 Chat with AI")
        
        # Simple text input for context
        st.markdown("### 📄 Add Context (Optional)")
        context_text = st.text_area(
            "Paste text content here:",
            placeholder="Paste any text you want to ask questions about...",
            height=150
        )
        
        # URL input
        url_input = st.text_input(
            "Or enter a URL:",
            placeholder="https://example.com/document.pdf"
        )
        
        if url_input and st.button("📥 Load from URL"):
            with st.spinner("Loading content from URL..."):
                extracted_text = extract_text_from_url(url_input)
                if extracted_text:
                    context_text = extracted_text
                    st.success("✅ Content loaded from URL!")
                else:
                    st.error("❌ Could not load content from URL")
        
        # Chat interface
        st.markdown("### 🤖 Ask Questions")
        user_question = st.text_input(
            "Your question:",
            placeholder="What is this document about?"
        )
        
        if st.button("Send 🚀") and user_question:
            if st.session_state.genai_model:
                try:
                    with st.spinner("🤔 Thinking..."):
                        # Prepare prompt with context
                        if context_text:
                            prompt = f"""
                            Based on the following context, please answer the question:
                            
                            Context: {context_text[:3000]}...
                            
                            Question: {user_question}
                            
                            Answer:"""
                        else:
                            prompt = user_question
                        
                        response = st.session_state.genai_model.generate_content(prompt)
                        
                        # Add to chat history
                        chat_entry = {
                            "question": user_question,
                            "answer": response.text,
                            "timestamp": time.time()
                        }
                        st.session_state.chat_history.append(chat_entry)
                        
                        # Display response
                        st.markdown("### 🤖 Response:")
                        st.markdown(response.text)
                        
                        if context_text:
                            st.info("💡 Response generated using your provided context")
                        
                except Exception as e:
                    st.error(f"❌ Error generating response: {str(e)}")
            else:
                st.error("❌ AI model not available")
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("### 📝 Chat History")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                with st.expander(f"Q{len(st.session_state.chat_history)-i}: {chat['question'][:50]}..."):
                    st.markdown(f"**Question:** {chat['question']}")
                    st.markdown(f"**Answer:** {chat['answer']}")
    
    with tab2:
        st.markdown("## 📄 Document Management")
        
        # File upload
        st.markdown("### 📤 Upload Documents")
        uploaded_files = st.file_uploader(
            "Choose text files",
            type=["txt", "md"],
            accept_multiple_files=True,
            help="Upload text files to use as context"
        )
        
        if uploaded_files:
            combined_text = ""
            for file in uploaded_files:
                content = file.read().decode('utf-8')
                combined_text += f"\n\n=== {file.name} ===\n{content}"
            
            st.text_area("Combined content:", combined_text, height=300)
            
            if st.button("📚 Use as Context"):
                st.session_state.document_context = combined_text
                st.success("✅ Documents loaded as context!")
        
        # Simple statistics
        if st.session_state.chat_history:
            st.markdown("### 📊 Simple Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Questions", len(st.session_state.chat_history))
            
            with col2:
                avg_q_length = sum(len(chat['question']) for chat in st.session_state.chat_history) / len(st.session_state.chat_history)
                st.metric("Avg Question Length", f"{avg_q_length:.0f} chars")
            
            with col3:
                avg_a_length = sum(len(chat['answer']) for chat in st.session_state.chat_history) / len(st.session_state.chat_history)
                st.metric("Avg Answer Length", f"{avg_a_length:.0f} chars")
    
    with tab3:
        st.markdown("## 🧪 AI Experiments")
        
        if not st.session_state.genai_model:
            st.warning("⚠️ Please set up API key first")
            return
        
        st.markdown("### 🌡️ Temperature Experiment")
        test_prompt = st.text_area(
            "Test prompt:",
            "Explain artificial intelligence in simple terms",
            height=100
        )
        
        if st.button("🧪 Run Experiment"):
            temperatures = [0.0, 0.5, 1.0]
            
            for temp in temperatures:
                st.markdown(f"#### Temperature: {temp}")
                
                try:
                    config = genai.types.GenerationConfig(temperature=temp)
                    response = st.session_state.genai_model.generate_content(
                        test_prompt,
                        generation_config=config
                    )
                    st.markdown(response.text)
                    st.markdown("---")
                except Exception as e:
                    st.error(f"Error with temperature {temp}: {str(e)}")
    
    with tab4:
        st.markdown("## 📊 Analytics")
        
        if not st.session_state.chat_history:
            st.info("📭 No data available. Start chatting to see analytics!")
            return
        
        # Basic analytics
        if PANDAS_AVAILABLE and PLOTLY_AVAILABLE:
            df = pd.DataFrame(st.session_state.chat_history)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Question length distribution
                df['question_length'] = df['question'].str.len()
                fig1 = px.histogram(df, x='question_length', title="Question Length Distribution")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Answer length distribution
                df['answer_length'] = df['answer'].str.len()
                fig2 = px.histogram(df, x='answer_length', title="Answer Length Distribution")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("⚠️ Advanced analytics require pandas and plotly")
            
            # Basic text analytics
            st.markdown("### 📈 Basic Statistics")
            
            total_questions = len(st.session_state.chat_history)
            total_chars_q = sum(len(chat['question']) for chat in st.session_state.chat_history)
            total_chars_a = sum(len(chat['answer']) for chat in st.session_state.chat_history)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Conversations", total_questions)
            
            with col2:
                st.metric("Total Question Chars", total_chars_q)
            
            with col3:
                st.metric("Total Answer Chars", total_chars_a)

if __name__ == "__main__":
    main()
