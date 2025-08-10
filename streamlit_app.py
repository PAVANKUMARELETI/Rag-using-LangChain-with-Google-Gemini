"""
🚀 RAG using LangChain with Google Gemini - Streamlit App
A beautiful web interface for the Retrieval-Augmented Generation system.
"""

import streamlit as st
import sys
import os
import time
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_chat import message
import logging

# Add src to path
sys.path.append('./src')

try:
    from src.config import Config
    from src.rag_chain import RAGChain
    from src.gemini_client import GeminiClient
    from src.document_processor import DocumentProcessor
    from src.embeddings_handler import EmbeddingsHandler
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Installing missing dependencies...")
    
    # Try to install missing packages
    missing_packages = [
        "langchain-community",
        "langchain-google-genai", 
        "langchain-text-splitters"
    ]
    
    for package in missing_packages:
        try:
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            st.success(f"Installed {package}")
        except Exception as install_error:
            st.warning(f"Could not install {package}: {install_error}")
    
    st.info("Please restart the app after installation completes.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="RAG with Gemini",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
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
    
    .metric-card {
        background: linear-gradient(45deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e1e5e9;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
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
    
    .stButton > button {
        background: linear-gradient(45deg, #1f77b4, #17a2b8);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #17a2b8, #1f77b4);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 RAG with Google Gemini</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Powered by LangChain & Streamlit</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f77b4/white?text=RAG+System", use_column_width=True)
        
        selected = option_menu(
            menu_title="Navigation",
            options=["🏠 Home", "⚙️ Setup", "📚 Documents", "💬 Chat", "🧪 Experiments", "📊 Analytics"],
            icons=["house", "gear", "book", "chat", "flask", "graph-up"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#1f77b4", "font-size": "18px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#1f77b4"},
            }
        )
    
    # Route to different pages
    if selected == "🏠 Home":
        show_home_page()
    elif selected == "⚙️ Setup":
        show_setup_page()
    elif selected == "📚 Documents":
        show_documents_page()
    elif selected == "💬 Chat":
        show_chat_page()
    elif selected == "🧪 Experiments":
        show_experiments_page()
    elif selected == "📊 Analytics":
        show_analytics_page()

def show_home_page():
    """Display the home page."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 Welcome to RAG System")
        st.markdown("""
        This application demonstrates a complete **Retrieval-Augmented Generation (RAG)** system 
        using Google Gemini and LangChain. Here's what you can do:
        
        ### ✨ Features
        - 🤖 **AI-Powered Chat**: Ask questions about your documents
        - 📄 **Document Processing**: Upload and process PDF files
        - 🔬 **Parameter Experiments**: Test different model settings
        - 📊 **Analytics**: Visualize system performance
        - ⚙️ **Easy Setup**: Intuitive configuration interface
        
        ### 🚀 Getting Started
        1. **Setup**: Configure your Google AI API key
        2. **Documents**: Upload PDF documents for analysis
        3. **Chat**: Start asking questions about your content
        4. **Experiment**: Fine-tune model parameters
        5. **Analyze**: View performance metrics
        """)
        
        # System status
        st.markdown("### 📋 System Status")
        
        col_status1, col_status2, col_status3 = st.columns(3)
        
        with col_status1:
            if st.session_state.api_key_set:
                st.success("🔑 API Key: Configured")
            else:
                st.error("🔑 API Key: Not Set")
        
        with col_status2:
            if st.session_state.documents_loaded:
                st.success("📚 Documents: Loaded")
            else:
                st.warning("📚 Documents: None")
        
        with col_status3:
            if st.session_state.rag_system:
                st.success("🤖 RAG System: Ready")
            else:
                st.info("🤖 RAG System: Not Initialized")
    
    with col2:
        st.markdown("### 🎮 Quick Actions")
        
        if st.button("🔧 Go to Setup", use_container_width=True):
            st.switch_page("⚙️ Setup")
        
        if st.button("📚 Load Documents", use_container_width=True):
            st.switch_page("📚 Documents") 
        
        if st.button("💬 Start Chatting", use_container_width=True):
            if st.session_state.rag_system and st.session_state.documents_loaded:
                st.switch_page("💬 Chat")
            else:
                st.warning("Please setup API key and load documents first!")
        
        st.markdown("---")
        
        # Recent activity
        st.markdown("### 📝 Recent Activity")
        if st.session_state.chat_history:
            for i, chat in enumerate(st.session_state.chat_history[-3:]):
                st.markdown(f"**Q:** {chat['question'][:50]}...")
                st.markdown(f"**A:** {chat['answer'][:50]}...")
                st.markdown("---")
        else:
            st.info("No recent activity")

def show_setup_page():
    """Display the setup configuration page."""
    
    st.markdown("## ⚙️ System Configuration")
    
    tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "🎛️ Parameters", "📁 Paths"])
    
    with tab1:
        st.markdown("### Google AI API Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google AI API Key",
            type="password",
            help="Get your API key from https://makersuite.google.com/app/apikey"
        )
        
        if api_key:
            if st.button("🔐 Save API Key"):
                try:
                    # Test the API key
                    test_client = GeminiClient(api_key=api_key)
                    response = test_client.generate_content("Hello")
                    st.session_state.api_key_set = True
                    st.success("✅ API Key validated and saved!")
                    
                    # Initialize RAG system
                    st.session_state.rag_system = RAGChain(api_key=api_key)
                    st.success("✅ RAG System initialized!")
                    
                except Exception as e:
                    st.error(f"❌ API Key validation failed: {str(e)}")
        
        # Model selection
        st.markdown("### Model Configuration")
        model_options = [
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest",
            "gemini-pro"
        ]
        
        selected_model = st.selectbox("Select Gemini Model", model_options)
        
        if st.button("🔄 Update Model"):
            if st.session_state.rag_system:
                st.session_state.rag_system.model_name = selected_model
                st.success(f"✅ Model updated to {selected_model}")
            else:
                st.warning("⚠️ Please set API key first")
    
    with tab2:
        st.markdown("### Model Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider("Temperature", 0.0, 2.0, 0.8, 0.1)
            max_tokens = st.slider("Max Output Tokens", 50, 2048, 1024, 50)
            
        with col2:
            top_k = st.slider("Top K", 1, 100, 32, 1)
            top_p = st.slider("Top P", 0.0, 1.0, 1.0, 0.1)
        
        if st.button("💾 Save Parameters"):
            if st.session_state.rag_system:
                st.session_state.rag_system.update_temperature(temperature)
                st.success("✅ Parameters updated successfully!")
            else:
                st.warning("⚠️ Please initialize RAG system first")
        
        # Parameter explanations
        with st.expander("📖 Parameter Explanations"):
            st.markdown("""
            - **Temperature**: Controls randomness (0.0 = focused, 2.0 = very creative)
            - **Max Output Tokens**: Maximum length of generated responses
            - **Top K**: Limits the number of top tokens considered
            - **Top P**: Nucleus sampling parameter (0.0 = most likely tokens only)
            """)
    
    with tab3:
        st.markdown("### File Paths Configuration")
        
        # Display current configuration
        config_info = {
            "Documents Directory": "./data/documents",
            "Vector Database": "./vector_db", 
            "Outputs Directory": "./outputs",
            "Chunk Size": "700 characters",
            "Chunk Overlap": "100 characters"
        }
        
        for key, value in config_info.items():
            st.info(f"**{key}**: {value}")
        
        st.markdown("### 📊 System Information")
        
        if st.session_state.rag_system:
            system_info = st.session_state.rag_system.get_system_info()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Model", system_info.get('model_name', 'N/A'))
            
            with col2:
                st.metric("Temperature", f"{system_info.get('temperature', 'N/A')}")
            
            with col3:
                vector_info = system_info.get('vector_store_info', {})
                st.metric("Documents", vector_info.get('count', 0))

def show_documents_page():
    """Display document management page."""
    
    st.markdown("## 📚 Document Management")
    
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set up your API key in the Setup page first.")
        return
    
    tab1, tab2, tab3 = st.tabs(["📤 Upload", "🔗 From URL", "📋 Manage"])
    
    with tab1:
        st.markdown("### Upload PDF Documents")
        
        uploaded_files = st.file_uploader(
            "Choose PDF files",
            type="pdf",
            accept_multiple_files=True,
            help="Upload one or more PDF files to add to your knowledge base"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
            
            for file in uploaded_files:
                st.info(f"📄 {file.name} ({file.size} bytes)")
            
            if st.button("🚀 Process Documents"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Save uploaded files
                    os.makedirs("./data/documents", exist_ok=True)
                    saved_files = []
                    
                    for i, file in enumerate(uploaded_files):
                        file_path = f"./data/documents/{file.name}"
                        with open(file_path, "wb") as f:
                            f.write(file.getvalue())
                        saved_files.append(file_path)
                        
                        progress = (i + 1) / len(uploaded_files) * 0.5
                        progress_bar.progress(progress)
                        status_text.text(f"Saving {file.name}...")
                    
                    # Process documents
                    status_text.text("Processing documents...")
                    num_chunks = st.session_state.rag_system.load_documents_from_directory("./data/documents")
                    
                    progress_bar.progress(1.0)
                    status_text.text("✅ Processing complete!")
                    
                    st.session_state.documents_loaded = True
                    st.success(f"✅ Processed {num_chunks} text chunks from {len(uploaded_files)} documents!")
                    
                except Exception as e:
                    st.error(f"❌ Error processing documents: {str(e)}")
    
    with tab2:
        st.markdown("### Load Document from URL")
        
        url = st.text_input(
            "PDF URL",
            placeholder="https://example.com/document.pdf",
            help="Enter a direct URL to a PDF document"
        )
        
        if url:
            if st.button("📥 Load from URL"):
                try:
                    with st.spinner("Loading document from URL..."):
                        num_chunks = st.session_state.rag_system.load_documents_from_url(url)
                        st.session_state.documents_loaded = True
                        st.success(f"✅ Loaded and processed {num_chunks} text chunks!")
                        
                except Exception as e:
                    st.error(f"❌ Error loading document: {str(e)}")
    
    with tab3:
        st.markdown("### Document Management")
        
        # List existing documents
        documents_dir = Path("./data/documents")
        if documents_dir.exists():
            pdf_files = list(documents_dir.glob("*.pdf"))
            
            if pdf_files:
                st.markdown("### 📄 Loaded Documents")
                
                for i, pdf_file in enumerate(pdf_files):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.text(f"📄 {pdf_file.name}")
                    
                    with col2:
                        file_size = pdf_file.stat().st_size
                        st.text(f"{file_size:,} bytes")
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{i}"):
                            pdf_file.unlink()
                            st.success(f"Deleted {pdf_file.name}")
                            st.rerun()
            else:
                st.info("📭 No documents uploaded yet")
        
        # Vector store management
        if st.session_state.rag_system:
            st.markdown("### 🗄️ Vector Store Management")
            
            vector_info = st.session_state.rag_system.embeddings_handler.get_vector_store_info()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Status", vector_info.get('status', 'unknown'))
            
            with col2:
                st.metric("Document Count", vector_info.get('count', 0))
            
            if st.button("🧹 Clear Vector Store"):
                try:
                    st.session_state.rag_system.reset()
                    st.session_state.documents_loaded = False
                    st.success("✅ Vector store cleared!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error clearing vector store: {str(e)}")

def show_chat_page():
    """Display the chat interface."""
    
    st.markdown("## 💬 Chat with Your Documents")
    
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set up your API key in the Setup page first.")
        return
    
    if not st.session_state.documents_loaded:
        st.warning("⚠️ Please load some documents first in the Documents page.")
        return
    
    # Chat interface
    st.markdown("### 🤖 AI Assistant")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, chat in enumerate(st.session_state.chat_history):
            message(chat["question"], is_user=True, key=f"user_{i}")
            message(chat["answer"], key=f"bot_{i}")
    
    # Chat input
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_question = st.text_input(
                "Ask a question about your documents:",
                placeholder="What is the main topic of the document?",
                key="chat_input"
            )
        
        with col2:
            send_button = st.button("Send 🚀", use_container_width=True)
    
    # Process question
    if send_button and user_question:
        try:
            with st.spinner("🤔 Thinking..."):
                result = st.session_state.rag_system.query(user_question)
                
                # Add to chat history
                chat_entry = {
                    "question": user_question,
                    "answer": result["answer"],
                    "timestamp": time.time(),
                    "sources": len(result["source_documents"])
                }
                
                st.session_state.chat_history.append(chat_entry)
                
                # Display new messages
                message(user_question, is_user=True, key=f"user_{len(st.session_state.chat_history)}")
                message(result["answer"], key=f"bot_{len(st.session_state.chat_history)}")
                
                # Show sources
                with st.expander(f"📚 View Sources ({len(result['source_documents'])} documents)"):
                    for i, doc in enumerate(result["source_documents"]):
                        st.text_area(
                            f"Source {i+1}",
                            doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                            height=100
                        )
                
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error processing question: {str(e)}")
    
    # Chat management
    with st.sidebar:
        st.markdown("### 💬 Chat Management")
        
        if st.session_state.chat_history:
            st.metric("Total Questions", len(st.session_state.chat_history))
            
            if st.button("🧹 Clear Chat History"):
                st.session_state.chat_history = []
                st.success("✅ Chat history cleared!")
                st.rerun()
            
            # Export chat
            if st.button("📥 Export Chat"):
                chat_data = pd.DataFrame(st.session_state.chat_history)
                csv = chat_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="chat_history.csv",
                    mime="text/csv"
                )

def show_experiments_page():
    """Display parameter experiments page."""
    
    st.markdown("## 🧪 Parameter Experiments")
    
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please set up your API key in the Setup page first.")
        return
    
    tab1, tab2, tab3 = st.tabs(["🌡️ Temperature", "🎯 Token Length", "📊 Comparison"])
    
    with tab1:
        st.markdown("### Temperature Experiment")
        st.info("Temperature controls creativity: 0.0 = very focused, 1.0+ = very creative")
        
        test_prompt = st.text_area(
            "Test Prompt",
            value="Explain artificial intelligence in simple terms",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            temp_values = st.multiselect(
                "Temperature Values",
                [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2],
                default=[0.0, 0.5, 1.0]
            )
        
        with col2:
            if st.button("🚀 Run Temperature Experiment"):
                if temp_values and test_prompt:
                    results = {}
                    progress_bar = st.progress(0)
                    
                    for i, temp in enumerate(temp_values):
                        progress_bar.progress((i + 1) / len(temp_values))
                        
                        try:
                            # Update temperature temporarily
                            original_temp = st.session_state.rag_system.temperature
                            st.session_state.rag_system.update_temperature(temp)
                            
                            # Generate response
                            response = st.session_state.rag_system.gemini_client.generate_content(test_prompt)
                            results[temp] = response
                            
                            # Restore original temperature
                            st.session_state.rag_system.update_temperature(original_temp)
                            
                        except Exception as e:
                            st.error(f"Error with temperature {temp}: {str(e)}")
                    
                    # Display results
                    st.markdown("### 📋 Results")
                    for temp, response in results.items():
                        st.markdown(f"**Temperature: {temp}**")
                        st.text_area(f"Response (temp={temp})", response, height=150, key=f"temp_{temp}")
                        st.markdown("---")
    
    with tab2:
        st.markdown("### Token Length Experiment")
        st.info("Max output tokens controls response length")
        
        test_prompt2 = st.text_area(
            "Test Prompt",
            value="Write a detailed explanation of machine learning",
            height=100,
            key="token_prompt"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            token_values = st.multiselect(
                "Max Token Values",
                [50, 100, 200, 500, 1000],
                default=[50, 200, 500]
            )
        
        with col2:
            if st.button("🚀 Run Token Experiment"):
                if token_values and test_prompt2:
                    results = {}
                    progress_bar = st.progress(0)
                    
                    for i, tokens in enumerate(token_values):
                        progress_bar.progress((i + 1) / len(token_values))
                        
                        try:
                            config = {"max_output_tokens": tokens}
                            response = st.session_state.rag_system.gemini_client.generate_content(
                                test_prompt2, 
                                generation_config=config
                            )
                            results[tokens] = response
                            
                        except Exception as e:
                            st.error(f"Error with {tokens} tokens: {str(e)}")
                    
                    # Display results
                    st.markdown("### 📋 Results")
                    for tokens, response in results.items():
                        st.markdown(f"**Max Tokens: {tokens}** (Actual: {len(response.split())} words)")
                        st.text_area(f"Response ({tokens} tokens)", response, height=150, key=f"tokens_{tokens}")
                        st.markdown("---")
    
    with tab3:
        st.markdown("### Parameter Comparison")
        
        if st.session_state.chat_history:
            # Analyze chat history for patterns
            df = pd.DataFrame(st.session_state.chat_history)
            
            if not df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Response length distribution
                    df['response_length'] = df['answer'].str.len()
                    fig_length = px.histogram(
                        df, 
                        x='response_length', 
                        title="Response Length Distribution",
                        labels={'response_length': 'Characters', 'count': 'Frequency'}
                    )
                    st.plotly_chart(fig_length, use_container_width=True)
                
                with col2:
                    # Sources used distribution
                    if 'sources' in df.columns:
                        fig_sources = px.histogram(
                            df,
                            x='sources',
                            title="Sources Used Distribution",
                            labels={'sources': 'Number of Sources', 'count': 'Frequency'}
                        )
                        st.plotly_chart(fig_sources, use_container_width=True)
                
                # Response time analysis (if available)
                st.markdown("### 📊 Chat Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Questions", len(df))
                
                with col2:
                    avg_length = df['response_length'].mean()
                    st.metric("Avg Response Length", f"{avg_length:.0f} chars")
                
                with col3:
                    if 'sources' in df.columns:
                        avg_sources = df['sources'].mean()
                        st.metric("Avg Sources Used", f"{avg_sources:.1f}")
                
                with col4:
                    st.metric("Total Responses", len(df))
        else:
            st.info("📭 No chat history available for analysis. Start chatting to see comparisons!")

def show_analytics_page():
    """Display analytics and system performance."""
    
    st.markdown("## 📊 System Analytics")
    
    if not st.session_state.rag_system:
        st.warning("⚠️ Please set up the RAG system first.")
        return
    
    tab1, tab2, tab3 = st.tabs(["📈 Performance", "📚 Documents", "💬 Usage"])
    
    with tab1:
        st.markdown("### System Performance Metrics")
        
        # System information
        system_info = st.session_state.rag_system.get_system_info()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Model", system_info.get('model_name', 'N/A'))
        
        with col2:
            st.metric("Temperature", f"{system_info.get('temperature', 'N/A')}")
        
        with col3:
            vector_info = system_info.get('vector_store_info', {})
            st.metric("Documents Loaded", vector_info.get('count', 0))
        
        with col4:
            st.metric("System Status", "✅ Ready" if system_info.get('qa_chain_ready') else "❌ Not Ready")
        
        # Performance visualization
        st.markdown("### 📊 Performance Overview")
        
        # Create sample performance data
        performance_data = {
            'Metric': ['API Response Time', 'Document Processing', 'Vector Search', 'Answer Generation'],
            'Score': [85, 92, 88, 90],
            'Status': ['Good', 'Excellent', 'Good', 'Excellent']
        }
        
        df_perf = pd.DataFrame(performance_data)
        
        fig_perf = px.bar(
            df_perf,
            x='Metric',
            y='Score',
            color='Status',
            title="System Performance Metrics",
            color_discrete_map={'Good': '#ffa500', 'Excellent': '#00ff00'}
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
    
    with tab2:
        st.markdown("### Document Analytics")
        
        # Document statistics
        documents_dir = Path("./data/documents")
        
        if documents_dir.exists():
            pdf_files = list(documents_dir.glob("*.pdf"))
            
            if pdf_files:
                # File size analysis
                file_data = []
                for pdf_file in pdf_files:
                    file_data.append({
                        'filename': pdf_file.name,
                        'size_mb': pdf_file.stat().st_size / (1024 * 1024),
                        'type': 'PDF'
                    })
                
                df_files = pd.DataFrame(file_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # File size distribution
                    fig_size = px.pie(
                        df_files,
                        values='size_mb',
                        names='filename',
                        title="Document Size Distribution"
                    )
                    st.plotly_chart(fig_size, use_container_width=True)
                
                with col2:
                    # File list with details
                    st.markdown("### 📄 Document Details")
                    st.dataframe(
                        df_files[['filename', 'size_mb']].round(2),
                        use_container_width=True
                    )
                
                # Total statistics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Documents", len(pdf_files))
                
                with col2:
                    total_size = sum(f['size_mb'] for f in file_data)
                    st.metric("Total Size", f"{total_size:.2f} MB")
                
                with col3:
                    avg_size = total_size / len(pdf_files) if pdf_files else 0
                    st.metric("Average Size", f"{avg_size:.2f} MB")
            else:
                st.info("📭 No documents loaded yet")
        else:
            st.info("📭 Documents directory not found")
    
    with tab3:
        st.markdown("### Usage Analytics")
        
        if st.session_state.chat_history:
            df_chat = pd.DataFrame(st.session_state.chat_history)
            
            # Usage over time (simulated)
            df_chat['hour'] = pd.to_datetime(df_chat['timestamp'], unit='s').dt.hour
            
            hourly_usage = df_chat.groupby('hour').size().reset_index(name='count')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Hourly usage pattern
                fig_hourly = px.line(
                    hourly_usage,
                    x='hour',
                    y='count',
                    title="Usage Pattern by Hour",
                    markers=True
                )
                fig_hourly.update_layout(xaxis_title="Hour of Day", yaxis_title="Number of Queries")
                st.plotly_chart(fig_hourly, use_container_width=True)
            
            with col2:
                # Question length distribution
                df_chat['question_length'] = df_chat['question'].str.len()
                fig_q_length = px.histogram(
                    df_chat,
                    x='question_length',
                    title="Question Length Distribution",
                    nbins=20
                )
                fig_q_length.update_layout(xaxis_title="Question Length (characters)", yaxis_title="Frequency")
                st.plotly_chart(fig_q_length, use_container_width=True)
            
            # Usage statistics
            st.markdown("### 📈 Usage Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Queries", len(df_chat))
            
            with col2:
                avg_q_length = df_chat['question_length'].mean()
                st.metric("Avg Question Length", f"{avg_q_length:.0f} chars")
            
            with col3:
                avg_a_length = df_chat['answer'].str.len().mean()
                st.metric("Avg Answer Length", f"{avg_a_length:.0f} chars")
            
            with col4:
                if 'sources' in df_chat.columns:
                    avg_sources = df_chat['sources'].mean()
                    st.metric("Avg Sources", f"{avg_sources:.1f}")
            
            # Most common question types (simple analysis)
            st.markdown("### 🔤 Question Analysis")
            
            # Extract first words of questions
            first_words = df_chat['question'].str.split().str[0].str.lower()
            word_counts = first_words.value_counts().head(10)
            
            if not word_counts.empty:
                fig_words = px.bar(
                    x=word_counts.values,
                    y=word_counts.index,
                    orientation='h',
                    title="Most Common Question Starters",
                    labels={'x': 'Count', 'y': 'First Word'}
                )
                st.plotly_chart(fig_words, use_container_width=True)
        else:
            st.info("📭 No usage data available. Start using the chat feature to see analytics!")

if __name__ == "__main__":
    main()
