# System Architecture

## Overview

The project is split into three main parts: the RAG system (handles documents and retrieval), the prompt engineering module (creates prompts and talks to the AI), and the web interface (what users see and interact with).

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

This handles all the document stuff - loading files, splitting them up, creating embeddings, and finding relevant chunks when you search.

**Key Components**:
- **Vector Store**: ChromaDB stores the document embeddings
- **Embeddings**: Uses OpenAI to create embeddings for semantic search
- **Text Splitter**: Splits documents into 1000 char chunks with 200 char overlap
- **Retrieval**: Finds the most similar chunks to your query

**How it works**:
1. You upload a document (PDF or TXT)
2. It gets split into chunks
3. Each chunk gets turned into an embedding (vector)
4. Embeddings are stored in ChromaDB
5. When you search, your query gets embedded too
6. It finds the most similar chunks and returns them

### 2. Prompt Engineering Module (`prompt_engineer.py`)

This is where the prompts are built. Different content types need different prompts, and this module handles that.

**Key Components**:
- **Base System Prompt**: Tells the AI what role to play
- **Content Type Prompts**: Specific instructions for each type (study guide, quiz, etc.)
- **Context Integration**: Takes the RAG context and adds it to the prompt
- **Edge Case Handling**: Checks for empty inputs, too long inputs, etc.

**Prompt Structure**:
```
System Message: You're an expert educational content creator
Human Message: 
  - What type of content to create
  - The topic
  - Relevant context from RAG (if using it)
  - Any extra requirements
```

### 3. Web Interface (`app.py`)

The Streamlit app that users interact with. Pretty straightforward - it's the UI.

**Features**:
- Content type selection
- Topic input
- Knowledge base management
- Document upload
- Content generation
- Download results

**User Flow**:
1. Click "Initialize Systems"
2. (Optional) Upload some documents
3. Pick what type of content you want
4. Enter your topic
5. Hit generate
6. Download if you like it

## Data Flow

### With RAG:

1. User enters topic and picks content type
2. RAG system searches knowledge base for relevant info
3. Prompt engineer builds a prompt with:
   - System prompt
   - Content type instructions
   - The topic
   - Retrieved context
   - Any extra requirements
4. Prompt goes to OpenAI
5. Content comes back and gets shown to user

### Without RAG:

1. User enters topic and picks content type
2. Prompt engineer builds a prompt (no context)
3. Prompt goes to OpenAI
4. Content comes back

## Technology Stack

- **Frontend**: Streamlit (super easy to use)
- **Backend**: Python 3.8+
- **LLM**: OpenAI GPT-3.5-turbo (can use GPT-4 too)
- **Vector Database**: ChromaDB (local, no setup needed)
- **Embeddings**: OpenAI Embeddings API
- **Document Processing**: LangChain (handles PDFs and text files)
- **Text Splitting**: LangChain's RecursiveCharacterTextSplitter

## File Structure

```
Final_Project/
├── app.py                      # Main app
├── rag_system.py              # RAG stuff
├── prompt_engineer.py         # Prompt handling
├── setup_knowledge_base.py    # Setup script
├── knowledge_base/            # Your documents
├── vector_store/              # ChromaDB storage (auto-created)
├── tests/                     # Tests
├── examples/                  # Example outputs
├── docs/                      # This documentation
└── web_page/                  # Project web page
```

## Scalability

- Vector store can handle a lot of documents (tested with 1000+)
- Chunking strategy works well for most cases
- Easy to add new content types
- Can switch between different AI models
- Knowledge base persists between sessions

## Security and Privacy

- API keys stored in .env file (not in code)
- No user data stored permanently
- Generated content is clearly marked as AI-generated
- Document sources are tracked in metadata
