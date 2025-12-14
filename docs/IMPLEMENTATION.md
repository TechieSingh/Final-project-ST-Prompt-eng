# Implementation Details

## RAG System

### Document Processing

1. **Loading**: PDF and TXT files using LangChain loaders
2. **Chunking**: 1000 character chunks with 200 character overlap
3. **Embeddings**: OpenAI text-embedding-ada-002 (1536 dimensions)
4. **Storage**: ChromaDB with local persistence
5. **Retrieval**: Similarity search returning top 5 results

### Design Choices

- **ChromaDB**: Easy setup, no external service needed
- **1000 char chunks**: Good balance of context and precision
- **200 char overlap**: Prevents information loss at boundaries

## Prompt Engineering

### Prompt Structure

- System message: Defines AI role as educational content creator
- Human message: Content type instructions, topic, RAG context, requirements

### Content Types

Each content type has specific instructions:
- Study Guide: Comprehensive, organized format
- Quiz: Questions with answers
- Explanation: Clear, detailed breakdown
- Summary: Concise key points
- Practice Problems: Problems with solutions

### Context Integration

- RAG context formatted with source numbers
- Explicit instructions to use context
- Fallback if context insufficient

### Error Handling

- Empty input validation
- Length limits (2000 chars)
- Basic content filtering
- API error handling

## Technology Stack

- Python 3.8+
- Streamlit
- LangChain
- OpenAI API
- ChromaDB
