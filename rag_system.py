"""
RAG (Retrieval-Augmented Generation) System

This module implements a RAG system for document storage and retrieval using:
- ChromaDB for vector storage
- OpenAI embeddings for text vectorization
- LangChain for document processing and chunking

The system allows users to:
- Load documents (PDF and TXT files)
- Split documents into chunks
- Create embeddings and store in vector database
- Retrieve relevant context based on queries
"""

import os
import shutil
from typing import List, Dict, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


class RAGSystem:
    """
    RAG System for document storage and retrieval.
    
    Handles document loading, chunking, embedding creation, and similarity search.
    Uses ChromaDB for persistent vector storage.
    """
    
    def __init__(self, persist_directory: str = "./vector_store", api_key: Optional[str] = None):
        """
        Initialize RAG system with vector store and embeddings.
        
        Args:
            persist_directory: Directory to store vector database
            api_key: OpenAI API key for embeddings (optional, can use env var)
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        
        # Text chunking settings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize or load existing ChromaDB vector store."""
        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except Exception as e:
            # Create new vector store if it doesn't exist
            try:
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
            except Exception:
                # Fallback: create without persist_directory
                self.vector_store = Chroma(
                    embedding_function=self.embeddings
                )
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a document from file path.
        
        Args:
            file_path: Path to PDF or TXT file
            
        Returns:
            List of Document objects
            
        Raises:
            ValueError: If file type is not supported
        """
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Can't handle this file type: {file_path}")
        
        documents = loader.load()
        return documents
    
    def add_documents(self, documents: List[Document], metadata: Optional[List[Dict]] = None):
        """
        Add documents to the knowledge base.
        
        Documents are split into chunks, embedded, and stored in vector database.
        
        Args:
            documents: List of Document objects to add
            metadata: Optional list of metadata dictionaries for each document
        """
        chunks = self.text_splitter.split_documents(documents)
        
        if metadata:
            for i, chunk in enumerate(chunks):
                if i < len(metadata):
                    chunk.metadata.update(metadata[i])
        
        self.vector_store.add_documents(chunks)
        # Persist is handled automatically in newer versions, but keep for compatibility
        try:
            self.vector_store.persist()
        except AttributeError:
            pass  # persist() not needed in newer versions
    
    def retrieve_relevant_context(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve most relevant documents for a query.
        
        Args:
            query: Search query string
            k: Number of documents to retrieve (default: 5)
            
        Returns:
            List of most relevant Document objects
        """
        if self.vector_store is None:
            return []
        
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        return [doc for doc, _ in docs[:k]]
    
    def get_context_string(self, query: str, k: int = 5) -> str:
        """
        Get formatted context string from retrieved documents.
        
        Args:
            query: Search query string
            k: Number of documents to retrieve
            
        Returns:
            Formatted string with retrieved context, or message if no context found
        """
        docs = self.retrieve_relevant_context(query, k)
        
        if not docs:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"[Source {i}]\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
    
    def clear_knowledge_base(self):
        """
        Clear all documents from the knowledge base.
        
        Removes the vector store directory and reinitializes an empty store.
        """
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        os.makedirs(self.persist_directory, exist_ok=True)
        self._initialize_vector_store()
