import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_system import RAGSystem
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def test_rag_initialization():
    print("Testing RAG system initialization...")
    rag = RAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
    assert rag.vector_store is not None
    print("RAG system initialized successfully")

def test_document_loading():
    print("Testing document loading...")
    rag = RAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
    
    test_doc = Document(
        page_content="This is a test document about machine learning. Machine learning is a subset of AI.",
        metadata={"source": "test.txt"}
    )
    
    rag.add_documents([test_doc])
    print("Document loaded and added successfully")

def test_retrieval():
    print("Testing document retrieval...")
    rag = RAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
    
    results = rag.retrieve_relevant_context("machine learning", k=3)
    print(f"Retrieved {len(results)} documents")
    
    return len(results) > 0

def test_context_string():
    print("Testing context string generation...")
    rag = RAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
    
    context = rag.get_context_string("machine learning", k=2)
    assert isinstance(context, str)
    print("Context string generated successfully")
    print(f"Context length: {len(context)} characters")

if __name__ == "__main__":
    print("Running RAG system tests...\n")
    
    try:
        test_rag_initialization()
        test_document_loading()
        test_retrieval()
        test_context_string()
        print("\nAll RAG tests passed!")
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        import traceback
        traceback.print_exc()
