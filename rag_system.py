import os
import shutil
from typing import List, Dict, Optional
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document


class RAGSystem:
    
    def __init__(self, persist_directory: str = "./vector_store", api_key: Optional[str] = None):
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
        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except Exception:
            # Create new vector store if it doesn't exist
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
    
    def load_document(self, file_path: str) -> List[Document]:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Can't handle this file type: {file_path}")
        
        documents = loader.load()
        return documents
    
    def add_documents(self, documents: List[Document], metadata: Optional[List[Dict]] = None):
        chunks = self.text_splitter.split_documents(documents)
        
        if metadata:
            for i, chunk in enumerate(chunks):
                if i < len(metadata):
                    chunk.metadata.update(metadata[i])
        
        self.vector_store.add_documents(chunks)
        self.vector_store.persist()
    
    def retrieve_relevant_context(self, query: str, k: int = 5) -> List[Document]:
        if self.vector_store is None:
            return []
        
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        return [doc for doc, _ in docs[:k]]
    
    def get_context_string(self, query: str, k: int = 5) -> str:
        docs = self.retrieve_relevant_context(query, k)
        
        if not docs:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            context_parts.append(f"[Source {i}]\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
    
    def clear_knowledge_base(self):
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        os.makedirs(self.persist_directory, exist_ok=True)
        self._initialize_vector_store()
