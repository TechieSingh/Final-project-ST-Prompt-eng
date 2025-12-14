# Educational Content Generator

A simple tool that generates educational content using RAG and prompt engineering.

## What it does

Generates educational materials like study guides, quizzes, explanations, summaries, and practice problems.

## How it works

The system uses RAG to search through uploaded documents and prompt engineering to generate different types of content. You can upload PDFs or text files to build a knowledge base, then generate content based on those documents.

### System Architecture

```mermaid
graph TB
    User[👤 User] -->|Interacts with| UI[Streamlit Web Interface<br/>app.py]
    
    UI -->|Calls| PE[Prompt Engineer<br/>prompt_engineer.py]
    UI -->|Calls| RAG[RAG System<br/>rag_system.py]
    
    PE -->|Sends prompts| OpenAI[OpenAI API<br/>GPT-3.5-turbo]
    RAG -->|Stores/Retrieves| ChromaDB[ChromaDB Vector Store<br/>Embeddings]
    RAG -->|Creates embeddings| EmbedAPI[OpenAI Embeddings API<br/>text-embedding-ada-002]
    
    OpenAI -->|Returns content| PE
    PE -->|Returns content| UI
    RAG -->|Returns context| UI
    UI -->|Displays| User
    
    style UI fill:#e1f5ff
    style PE fill:#fff4e1
    style RAG fill:#e8f5e9
    style OpenAI fill:#f3e5f5
    style ChromaDB fill:#fff9c4
    style EmbedAPI fill:#f3e5f5
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

3. Initialize knowledge base (optional):
```bash
python setup_knowledge_base.py
```

4. Run the app:
```bash
streamlit run app.py
```

## Usage

1. Run `streamlit run app.py`
2. Click "Initialize Systems" in the sidebar
3. Upload documents if you want (optional)
4. Select content type and enter topic
5. Click generate

## Project Structure

- `app.py` - Main Streamlit app
- `rag_system.py` - Handles document storage and retrieval
- `prompt_engineer.py` - Creates prompts and calls OpenAI API
- `knowledge_base/` - Upload your documents here
- `tests/` - Test files
- `docs/` - Documentation

## Documentation

- [Project Documentation](docs/PROJECT_DOCUMENTATION.md) - Complete documentation
- [Web Page](web_page/index.html) - Project showcase

## Testing

```bash
python tests/test_rag.py
python tests/test_prompts.py
```
