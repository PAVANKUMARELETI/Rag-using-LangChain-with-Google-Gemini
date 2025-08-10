# 🌐 Streamlit App User Guide

Welcome to the beautiful RAG (Retrieval-Augmented Generation) web application! This guide will help you get the most out of the system.

## 🚀 Getting Started

### Launch Options

**Option 1: Quick Launch (Windows)**
```bash
run_app.bat
```
Double-click the batch file for instant launch!

**Option 2: Python Script**
```bash
python run_app.py
```

**Option 3: Direct Streamlit**
```bash
streamlit run streamlit_app.py
```

### First Time Setup
1. 🔑 Navigate to **Setup** page
2. 📝 Enter your Google AI API key
3. ✅ Click "Save API Key" to validate
4. 🎯 Optionally adjust model parameters

## 📖 Page-by-Page Guide

### 🏠 Home Page
Your central dashboard showing:
- **System Status**: API key, documents, RAG system readiness
- **Quick Actions**: Direct links to key functions
- **Recent Activity**: Your latest chat interactions
- **Feature Overview**: What you can accomplish

**Pro Tips:**
- Check system status before starting
- Use quick actions for rapid navigation
- Monitor recent activity for context

### ⚙️ Setup Page

#### 🔑 API Keys Tab
- **Google AI API Key**: Enter and validate your key
- **Model Selection**: Choose between Gemini models
- **Test Connection**: Automatic validation on save

#### 🎛️ Parameters Tab
- **Temperature**: 0.0 (focused) → 2.0 (creative)
- **Max Output Tokens**: Response length limit
- **Top K**: Vocabulary restriction (1-100)
- **Top P**: Nucleus sampling (0.0-1.0)

#### 📁 Paths Tab
- **Directory Settings**: View file locations
- **System Information**: Current configuration
- **Performance Metrics**: Live system status

**Pro Tips:**
- Start with default parameters
- Save API key before proceeding
- Adjust temperature based on use case

### 📚 Documents Page

#### 📤 Upload Tab
- **Multi-file Upload**: Drag & drop PDFs
- **Progress Tracking**: Real-time processing updates
- **Batch Processing**: Handle multiple documents

#### 🔗 From URL Tab
- **Direct Loading**: Paste PDF URLs
- **Instant Processing**: No download required
- **Remote Access**: Access online documents

#### 📋 Manage Tab
- **File Browser**: View loaded documents
- **Size Analytics**: Monitor storage usage
- **Vector Store**: Manage embeddings database
- **Cleanup Tools**: Remove unwanted files

**Pro Tips:**
- Use clear, text-based PDFs
- Keep files under 50MB for best performance
- Load related documents together

### 💬 Chat Page

#### Chat Interface Features
- **Real-time Responses**: Instant AI interaction
- **Source Attribution**: See which documents inform answers
- **Chat History**: Persistent conversation memory
- **Context Awareness**: References previous messages

#### Chat Management
- **Export History**: Download conversations as CSV
- **Clear History**: Start fresh conversations
- **Session Metrics**: Track usage statistics
- **Source Inspection**: Examine referenced content

**Pro Tips:**
- Ask specific questions for better results
- Use follow-up questions to dive deeper
- Check sources to verify information
- Export important conversations

### 🧪 Experiments Page

#### 🌡️ Temperature Experiments
- **Multi-value Testing**: Compare different creativity levels
- **Side-by-side Results**: Visual comparison
- **Response Analysis**: See creativity impact
- **Custom Prompts**: Test with your content

#### 🎯 Token Length Experiments
- **Response Length Testing**: Compare output sizes
- **Word Count Analysis**: Track actual vs. target length
- **Efficiency Metrics**: Optimize for your needs
- **Batch Comparisons**: Multiple length settings

#### 📊 Parameter Comparison
- **Historical Analysis**: Your chat patterns
- **Response Metrics**: Length and source distributions
- **Usage Patterns**: When you're most active
- **Performance Trends**: System efficiency over time

**Pro Tips:**
- Start with temperature experiments
- Use consistent test prompts
- Document your best settings
- Compare results systematically

### 📊 Analytics Page

#### 📈 Performance Tab
- **System Metrics**: Response time, processing speed
- **Component Status**: Individual system health
- **Performance Scores**: Comparative ratings
- **Real-time Monitoring**: Live system stats

#### 📚 Documents Tab
- **Storage Analysis**: File size distributions
- **Document Statistics**: Count, size, type breakdown
- **Usage Patterns**: Which documents get used most
- **Optimization Insights**: Storage recommendations

#### 💬 Usage Tab
- **Activity Patterns**: When you use the system most
- **Question Analysis**: Common question types
- **Response Statistics**: Average lengths and sources
- **Trend Analysis**: Usage over time

**Pro Tips:**
- Monitor performance regularly
- Use analytics to optimize parameters
- Track usage patterns for insights
- Export data for external analysis

## 🎯 Best Practices

### For Best Results
1. **Document Quality**: Use clear, well-formatted PDFs
2. **Specific Questions**: Ask precise, focused questions
3. **Parameter Tuning**: Adjust settings based on needs
4. **Context Building**: Load related documents together

### Troubleshooting
1. **Slow Performance**: Reduce document size or chunk count
2. **Poor Answers**: Check document relevance and quality
3. **No Results**: Verify documents loaded successfully
4. **Connection Issues**: Validate API key in Setup

### Performance Optimization
1. **Temperature**: 0.2-0.4 for factual, 0.6-0.8 for creative
2. **Chunk Size**: 500-1000 characters optimal
3. **Document Count**: 5-10 related documents work well
4. **Question Length**: 10-50 words usually optimal

## 🔧 Advanced Features

### Custom Configurations
- **Environment Variables**: Use .env file for settings
- **Theme Customization**: Modify .streamlit/config.toml
- **Parameter Presets**: Save common configurations
- **Batch Operations**: Process multiple documents

### Integration Options
- **API Access**: Use src modules programmatically
- **Export Functions**: Save results in various formats
- **Automation**: Script common operations
- **Monitoring**: Track system metrics

## 🛠️ Troubleshooting Guide

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "API Key Error" | Invalid/missing key | Check Setup page, validate key |
| "No documents loaded" | Empty document store | Upload PDFs in Documents page |
| "Slow responses" | Large documents | Reduce chunk size in config |
| "Generic answers" | Poor document match | Rephrase question, check sources |
| "App won't start" | Missing dependencies | Run `pip install -r requirements.txt` |

### Performance Issues
- **High Memory Usage**: Reduce loaded documents
- **Slow Loading**: Check internet connection for URL docs
- **Timeout Errors**: Increase timeout in config
- **Storage Full**: Clean up vector database

### Getting Help
1. **Check System Status** on Home page
2. **Review Analytics** for insights
3. **Experiment** with different parameters
4. **Export Data** for external analysis
5. **Restart App** if issues persist

## 📱 Mobile & Tablet Usage

The app is responsive and works on mobile devices:
- **Touch-friendly**: Large buttons and touch targets
- **Responsive Layout**: Adapts to screen size
- **Mobile Chat**: Optimized conversation interface
- **Gesture Support**: Swipe and tap interactions

## 🎨 Customization

### Theme Options
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"  # Your brand color
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

### Feature Toggles
- **Debug Mode**: Enable detailed error messages
- **Analytics**: Turn on/off usage tracking
- **Caching**: Configure response caching
- **Logging**: Adjust log levels

---

## 🚀 Happy Exploring!

The RAG system is powerful and flexible. Start with the basics and gradually explore advanced features. The combination of document intelligence and conversational AI opens up endless possibilities!

**Questions? Issues? Suggestions?**
Check the main README.md for additional resources and support options.

*Built with ❤️ using Streamlit, LangChain, and Google Gemini*
