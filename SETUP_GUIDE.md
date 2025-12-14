# Setup Guide

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with your OpenAI API key: `OPENAI_API_KEY=your_key`
3. Initialize knowledge base (optional): `python setup_knowledge_base.py`
4. Run app: `streamlit run app.py`

## Troubleshooting

- **API key not found**: Make sure `.env` file exists in project root
- **Module not found**: Run `pip install -r requirements.txt` again
- **ChromaDB errors**: Delete `vector_store/` directory and reinitialize

## Testing

```bash
python tests/test_rag.py
python tests/test_prompts.py
```
