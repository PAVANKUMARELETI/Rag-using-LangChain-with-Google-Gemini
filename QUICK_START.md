# Quick Start Guide - RAG using LangChain with Google Gemini

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google AI API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this project**

2. **Run the installation script:**
   ```bash
   python install.py
   ```

3. **Set up your API key:**
   - Edit `config/.env`
   - Replace `your_google_ai_api_key_here` with your actual API key

4. **Start the notebook:**
   ```bash
   jupyter notebook app.ipynb
   ```

## 📚 Project Structure

```
RAG using LangChain with Google Gemini/
├── app.ipynb              # Main tutorial notebook
├── src/                   # Modular code
│   ├── config.py         # Configuration management
│   ├── gemini_client.py  # Gemini API wrapper
│   ├── document_processor.py # PDF processing
│   ├── embeddings_handler.py # Vector embeddings
│   └── rag_chain.py      # Complete RAG system
├── data/documents/        # Place your PDF files here
├── config/.env           # Your API keys and settings
└── requirements.txt      # Python dependencies
```

## 🎯 Tutorial Tasks

### Phase 1: Introduction (Tasks 0-1)
- Get started with the environment
- Import necessary libraries

### Phase 2: Interact with Google Gemini (Tasks 2-3)
- Basic text generation with prompts
- Chat functionality and history retrieval

### Phase 3: Parameter Experimentation (Tasks 4-8)
- Temperature: Controls randomness (0.0 = focused, 1.0 = creative)
- Max Output Tokens: Limits response length
- Top-k: Limits vocabulary choices
- Top-p: Nucleus sampling parameter
- Candidate Count: Number of response alternatives

### Phase 4: RAG System (Tasks 9-13)
- Introduction to Retrieval-Augmented Generation
- PDF document loading and processing
- Vector embeddings creation
- Complete RAG chain implementation
- Modular system usage

## 🔧 Key Features

### Simple Text Generation
```python
import google.generativeai as genai

genai.configure(api_key='your-api-key')
model = genai.GenerativeModel('gemini-1.5-flash-latest')
response = model.generate_content("Explain machine learning")
print(response.text)
```

### RAG System Usage
```python
from src.rag_chain import RAGChain

# Initialize
rag = RAGChain(api_key='your-api-key')

# Load documents
rag.load_documents_from_url('http://example.com/document.pdf')

# Ask questions
answer = rag.query("What is the main topic of this document?")
print(answer['answer'])
```

### Parameter Tuning
```python
# Experiment with temperature
results = gemini_client.experiment_temperature(
    "Explain artificial intelligence",
    [0.0, 0.5, 1.0]
)
```

## 🛠️ Configuration

Edit `config/.env` to customize:

```env
# API Configuration
GOOGLE_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-1.5-flash-latest

# Text Processing
CHUNK_SIZE=700
CHUNK_OVERLAP=100

# Model Parameters  
DEFAULT_TEMPERATURE=0.8
DEFAULT_MAX_OUTPUT_TOKENS=1024
```

## 💡 Tips & Best Practices

### For Better Results:
1. **Temperature**: Use 0.0-0.3 for factual answers, 0.7-1.0 for creative content
2. **Chunk Size**: 500-1000 characters work well for most documents
3. **Similarity Search**: Use k=3-5 for most queries

### Common Issues:
1. **API Key Error**: Make sure your Google AI API key is correctly set
2. **Memory Issues**: Reduce chunk size for large documents
3. **No Results**: Check if documents were loaded successfully

## 📖 Learning Path

### Beginner
1. Complete Tasks 0-3 (Basic Gemini interaction)
2. Try different prompts and see responses
3. Explore chat functionality

### Intermediate  
4. Complete Tasks 4-8 (Parameter experiments)
5. Understand how parameters affect output
6. Try your own parameter combinations

### Advanced
7. Complete Tasks 9-13 (RAG system)
8. Load your own PDF documents
9. Build custom RAG applications

## 🔍 Troubleshooting

### Installation Issues
```bash
# If pip install fails, try:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# For Windows users:
pip install --user -r requirements.txt
```

### API Issues
- Verify your API key is active at [Google AI Studio](https://makersuite.google.com/)
- Check quota limits and usage
- Ensure you have enabled the necessary APIs

### Document Loading Issues
- Ensure PDF files are accessible and not corrupted
- Check file paths are correct
- For large files, consider splitting them

## 🎓 Next Steps

After completing this tutorial:
1. Build your own RAG application with custom documents
2. Experiment with different embedding models
3. Try other LangChain features like agents and tools
4. Deploy your RAG system to production

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the notebook comments and documentation
3. Refer to [LangChain docs](https://python.langchain.com/)
4. Check [Google AI documentation](https://ai.google.dev/)

## 📄 License

This project is for educational purposes. Please check:
- Google AI terms of service for API usage
- LangChain license for commercial use
- Individual library licenses in requirements.txt

Happy learning! 🎉
