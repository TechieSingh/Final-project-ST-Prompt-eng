# System Architecture

## Overview

The Educational Content Generator is built using a modular architecture that separates concerns into distinct components: RAG (Retrieval-Augmented Generation) system, Prompt Engineering module, and Web Interface.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                  │
│                         (app.py)                            │
└────────────┬──────────────────────────────┬────────────────┘
             │                              │
             ▼                              ▼
┌────────────────────────┐    ┌──────────────────────────────┐
│   Prompt Engineer      │    │      RAG System               │
│  (prompt_engineer.py)   │    │    (rag_system.py)           │
│                        │    │                              │
│ - Content Type Prompts │    │ - Document Loading            │
│ - Context Management   │    │ - Text Chunking              │
│ - Edge Case Handling   │    │ - Vector Embeddings          │
│ - LLM Integration      │    │ - Similarity Search          │
└────────────┬───────────┘    └──────────────┬───────────────┘
             │                                │
             │                                │
             ▼                                ▼
┌────────────────────────┐    ┌──────────────────────────────┐
│   OpenAI API           │    │   ChromaDB Vector Store      │
│   (GPT Models)         │    │   (Embeddings Storage)       │
└────────────────────────┘    └──────────────────────────────┘
```

## Component Details

### 1. RAG System (`rag_system.py`)

**Purpose**: Manages knowledge base and document retrieval

**Key Components**:
- **Vector Store**: ChromaDB for storing document embeddings
- **Embeddings**: OpenAI embeddings for semantic search
- **Text Splitter**: RecursiveCharacterTextSplitter with 1000 char chunks, 200 char overlap
- **Retrieval**: Similarity search with relevance filtering

**Data Flow**:
1. Documents loaded from files (PDF, TXT)
2. Documents split into chunks
3. Chunks embedded using OpenAI embeddings
4. Embeddings stored in ChromaDB
5. Queries embedded and matched against stored embeddings
6. Top-k most similar chunks retrieved

### 2. Prompt Engineering Module (`prompt_engineer.py`)

**Purpose**: Manages systematic prompt generation and LLM interaction

**Key Components**:
- **Base System Prompt**: Defines AI role and constraints
- **Content Type Prompts**: Specialized prompts for each content type
- **Context Integration**: Dynamically incorporates RAG context
- **Edge Case Handling**: Validates and handles problematic inputs

**Prompt Structure**:
```
System Message: Role definition and constraints
Human Message: 
  - Content type specific instructions
  - Topic
  - Retrieved context (if using RAG)
  - Additional requirements
```

### 3. Web Interface (`app.py`)

**Purpose**: User-facing application built with Streamlit

**Features**:
- Content type selection
- Topic input
- Knowledge base management
- Document upload
- Content generation
- Result display and download

**User Flow**:
1. Initialize systems
2. (Optional) Upload documents to knowledge base
3. Select content type
4. Enter topic
5. Generate content
6. View and download results

## Data Flow

### Content Generation with RAG:

1. User inputs topic and selects content type
2. RAG system retrieves relevant context from knowledge base
3. Prompt engineer constructs prompt with:
   - System prompt
   - Content type instructions
   - Topic
   - Retrieved context
   - Additional requirements
4. Prompt sent to OpenAI API
5. Generated content returned to user

### Content Generation without RAG:

1. User inputs topic and selects content type
2. Prompt engineer constructs prompt without context
3. Prompt sent to OpenAI API
4. Generated content returned to user

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **LLM**: OpenAI GPT-3.5-turbo / GPT-4
- **Vector Database**: ChromaDB
- **Embeddings**: OpenAI Embeddings API
- **Document Processing**: LangChain (PyPDF, TextLoader)
- **Text Splitting**: LangChain RecursiveCharacterTextSplitter

## File Structure

```
Final_Project/
├── app.py                      # Main Streamlit application
├── rag_system.py              # RAG implementation
├── prompt_engineer.py         # Prompt engineering
├── setup_knowledge_base.py    # KB initialization
├── knowledge_base/            # Source documents
├── vector_store/              # ChromaDB storage
├── tests/                     # Test scripts
├── examples/                  # Example outputs
├── docs/                      # Documentation
└── web_page/                  # Project web page
```

## Scalability Considerations

- Vector store can handle thousands of documents
- Chunking strategy optimized for retrieval quality
- Modular design allows easy addition of new content types
- API-based LLM allows switching between models
- Persistent storage enables knowledge base reuse

## Security and Privacy

- API keys stored in environment variables
- No user data stored permanently
- Generated content clearly marked as AI-generated
- Document sources tracked in metadata

