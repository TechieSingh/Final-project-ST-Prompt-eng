# Educational Content Generator

An AI system that creates educational content using RAG and prompt engineering.

## Overview

This project generates educational materials including:
- Study guides
- Quiz questions
- Concept explanations
- Summaries
- Practice problems

## Components

### RAG System
- Knowledge base using ChromaDB
- Document chunking and embedding
- Retrieval and ranking mechanisms
- Supports PDF and TXT files

### Prompt Engineering
- Specialized prompts for different content types
- Context management
- Error handling

## Features

- Web interface built with Streamlit
- Multiple content types
- Knowledge base management
- Context-aware generation using RAG
- Customizable prompts

## Setup

### Requirements
- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Final_Project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```
OPENAI_API_KEY=your_api_key_here
```

4. Initialize the knowledge base:
```bash
python setup_knowledge_base.py
```

5. Run the application:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
Final_Project/
├── app.py                      # Main application
├── rag_system.py              # RAG implementation
├── prompt_engineer.py         # Prompt engineering
├── knowledge_base/            # Knowledge base documents
├── vector_store/             # Vector database
├── setup_knowledge_base.py   # Setup script
├── tests/                    # Tests
├── examples/                 # Example outputs
├── docs/                     # Documentation
├── web_page/                 # Web page
└── requirements.txt          # Dependencies
```

## Usage

1. Start the app: `streamlit run app.py`
2. Upload documents (optional) to the knowledge base
3. Select content type
4. Enter topic
5. Generate content

## Testing

Run tests:
```bash
python tests/test_rag.py
python tests/test_prompts.py
```

## Documentation

See the `docs/` directory for:
- Architecture details
- Implementation guide
- Performance metrics

## Ethical Considerations

- Generated content is marked as AI-generated
- Sources are tracked and can be cited
- Content filtering for inappropriate material
- Privacy considerations for user data
