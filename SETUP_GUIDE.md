# Complete Setup Guide

## Quick Start

1. **Install Python 3.8+** (if not already installed)
2. **Clone or download this repository**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Set up API key**: Create `.env` file with `OPENAI_API_KEY=your_key`
5. **Initialize knowledge base**: `python setup_knowledge_base.py`
6. **Run application**: `streamlit run app.py`

## Detailed Setup Instructions

### Step 1: Python Environment

Ensure Python 3.8 or higher is installed:
```bash
python --version
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: OpenAI API Key

1. Get an API key from https://platform.openai.com/api-keys
2. Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Initialize Knowledge Base

Run the setup script to add sample documents:
```bash
python setup_knowledge_base.py
```

This will create the vector store with sample educational content.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Troubleshooting

### Issue: "OpenAI API key not found"
- Ensure `.env` file exists in project root
- Check that API key is correctly formatted
- Restart the application after creating `.env`

### Issue: "Module not found"
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

### Issue: "ChromaDB errors"
- Delete `vector_store/` directory and reinitialize
- Run `python setup_knowledge_base.py` again

### Issue: "API rate limit exceeded"
- Wait a few minutes and try again
- Check your OpenAI account usage limits
- Consider using a different API key

## Testing

Run test scripts to verify installation:
```bash
python tests/test_rag.py
python tests/test_prompts.py
```

## Next Steps

1. Upload your own documents to the knowledge base
2. Try generating different content types
3. Experiment with different topics
4. Review generated content and provide feedback

## Support

For issues or questions:
1. Check the README.md
2. Review documentation in `docs/` directory
3. Check GitHub issues (if repository is public)

