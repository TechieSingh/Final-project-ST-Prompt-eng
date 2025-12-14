import os
from rag_system import RAGSystem
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def setup_sample_knowledge_base():
    print("Setting up knowledge base...")
    
    rag = RAGSystem(api_key=os.getenv("OPENAI_API_KEY"))
    
    # some sample docs to get started
    sample_documents = [
        {
            "content": """
            Introduction to Machine Learning
            
            Machine Learning is a subset of artificial intelligence that enables systems to learn 
            and improve from experience without being explicitly programmed. It focuses on the 
            development of computer programs that can access data and use it to learn for themselves.
            
            Key Concepts:
            1. Supervised Learning: Learning with labeled data
            2. Unsupervised Learning: Finding patterns in unlabeled data
            3. Reinforcement Learning: Learning through interaction and rewards
            
            Applications include image recognition, natural language processing, and recommendation systems.
            """,
            "metadata": {"source": "sample_ml_intro.txt", "topic": "Machine Learning"}
        },
        {
            "content": """
            Python Programming Basics
            
            Python is a high-level, interpreted programming language known for its simplicity and readability.
            
            Key Features:
            - Dynamic typing
            - Automatic memory management
            - Extensive standard library
            - Support for multiple programming paradigms
            
            Basic Syntax:
            - Variables: x = 10
            - Functions: def my_function():
            - Loops: for i in range(10):
            - Conditionals: if condition:
            
            Python is widely used in web development, data science, and AI applications.
            """,
            "metadata": {"source": "sample_python.txt", "topic": "Python Programming"}
        },
        {
            "content": """
            Photosynthesis Process
            
            Photosynthesis is the process by which plants convert light energy into chemical energy.
            
            The process occurs in two main stages:
            1. Light-dependent reactions: Capture light energy and convert it to ATP and NADPH
            2. Light-independent reactions (Calvin Cycle): Use ATP and NADPH to produce glucose
            
            Key Equation: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2
            
            Factors affecting photosynthesis:
            - Light intensity
            - Carbon dioxide concentration
            - Temperature
            - Water availability
            
            This process is essential for life on Earth as it produces oxygen and organic compounds.
            """,
            "metadata": {"source": "sample_photosynthesis.txt", "topic": "Biology"}
        }
    ]
    
    documents = []
    for doc_data in sample_documents:
        doc = Document(
            page_content=doc_data["content"],
            metadata=doc_data["metadata"]
        )
        documents.append(doc)
    
    rag.add_documents(documents)
    
    print("Knowledge base initialized with sample documents!")
    print(f"Added {len(documents)} documents to the knowledge base")

if __name__ == "__main__":
    setup_sample_knowledge_base()
