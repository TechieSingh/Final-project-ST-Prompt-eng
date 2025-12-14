# System Architecture

## Overview

The project has three main parts: RAG system (handles documents), prompt engineering (creates prompts), and web interface (user interaction).

## Architecture

### System Architecture Diagram

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

## Components

### 1. RAG System (rag_system.py)

Handles document loading, chunking, embedding, and retrieval.

**How it works:**
1. Upload document (PDF or TXT)
2. Split into chunks (1000 chars, 200 overlap)
3. Create embeddings using OpenAI
4. Store in ChromaDB
5. When searching, embed query and find similar chunks

### 2. Prompt Engineering (prompt_engineer.py)

Builds prompts for different content types and integrates RAG context.

**Prompt Structure:**
- System message: Defines AI role
- Human message: Content type, topic, context from RAG, requirements

### 3. Web Interface (app.py)

Streamlit app for user interaction.

**Features:**
- Content type selection
- Document upload
- Topic input
- Content generation
- Download results

## Technology Stack

- Python 3.8+
- Streamlit
- LangChain
- OpenAI API
- ChromaDB

## Data Flow

**With RAG:**
1. User enters topic
2. RAG searches knowledge base
3. Prompt engineer builds prompt with context
4. Send to OpenAI
5. Display result

**Without RAG:**
1. User enters topic
2. Prompt engineer builds prompt (no context)
3. Send to OpenAI
4. Display result
