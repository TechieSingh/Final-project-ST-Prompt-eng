import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from rag_system import RAGSystem
from prompt_engineer import PromptEngineer

load_dotenv()

st.set_page_config(
    page_title="Educational Content Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'prompt_engineer' not in st.session_state:
    st.session_state.prompt_engineer = None
if 'knowledge_base_initialized' not in st.session_state:
    st.session_state.knowledge_base_initialized = False

def initialize_systems():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        return False
    
    try:
        if st.session_state.rag_system is None:
            st.session_state.rag_system = RAGSystem(api_key=api_key)
        
        if st.session_state.prompt_engineer is None:
            st.session_state.prompt_engineer = PromptEngineer(api_key=api_key)
        
        st.session_state.knowledge_base_initialized = True
        return True
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
        return False

def main():
    st.title("Educational Content Generator")
    st.markdown("Create study guides, quizzes, explanations, and more using AI")
    
    with st.sidebar:
        st.header("Configuration")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.success("API Key configured")
        else:
            st.error("API Key not found")
        
        if st.button("Initialize Systems", type="primary"):
            with st.spinner("Initializing..."):
                if initialize_systems():
                    st.success("Ready!")
                    st.rerun()
        
        st.divider()
        
        st.header("Knowledge Base")
        
        if st.session_state.knowledge_base_initialized:
            st.success("Knowledge Base Ready")
            
            uploaded_files = st.file_uploader(
                "Upload Documents",
                type=['pdf', 'txt'],
                accept_multiple_files=True
            )
            
            if uploaded_files and st.button("Add to Knowledge Base"):
                with st.spinner("Processing..."):
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        try:
                            docs = st.session_state.rag_system.load_document(tmp_path)
                            st.session_state.rag_system.add_documents(docs)
                            st.success(f"Added {uploaded_file.name}")
                        except Exception as e:
                            st.error(f"Couldn't process {uploaded_file.name}: {str(e)}")
                        finally:
                            os.unlink(tmp_path)
            
            if st.button("Clear Knowledge Base", type="secondary"):
                st.session_state.rag_system.clear_knowledge_base()
                st.success("Cleared!")
                st.rerun()
        else:
            st.info("Initialize systems first")
    
    if not st.session_state.knowledge_base_initialized:
        st.info("Please initialize systems from the sidebar to begin")
        return
    
    st.header("Generate Educational Content")
    
    content_types = {
        "Study Guide": "study_guide",
        "Quiz Questions": "quiz",
        "Concept Explanation": "explanation",
        "Summary": "summary",
        "Practice Problems": "practice_problems"
    }
    
    selected_type = st.selectbox(
        "Select Content Type",
        options=list(content_types.keys())
    )
    
    content_type = content_types[selected_type]
    
    topic = st.text_input(
        "Enter Topic or Subject",
        placeholder="e.g., Photosynthesis, Python Functions, World War II"
    )
    
    additional_requirements = st.text_area(
        "Additional Requirements (Optional)",
        placeholder="e.g., Make it suitable for high school students, Include examples"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        use_rag = st.checkbox("Use Knowledge Base (RAG)", value=True)
    with col2:
        show_context = st.checkbox("Show Retrieved Context", value=False)
    
    if st.button("Generate Content", type="primary", use_container_width=True):
        if not topic:
            st.error("Please enter a topic")
            return
        
        error_msg = st.session_state.prompt_engineer.handle_edge_cases(topic)
        if error_msg:
            st.warning(error_msg)
            return
        
        with st.spinner("Working on it..."):
            if use_rag:
                result = st.session_state.prompt_engineer.generate_with_rag(
                    content_type=content_type,
                    topic=topic,
                    rag_system=st.session_state.rag_system,
                    additional_requirements=additional_requirements if additional_requirements else None
                )
                
                if show_context and result.get("context_used"):
                    with st.expander("Retrieved Context from Knowledge Base"):
                        st.text(result["context_used"])
                
                st.subheader("Generated Content")
                st.markdown(result["content"])
                
                st.download_button(
                    label="Download Content",
                    data=result["content"],
                    file_name=f"{content_type}_{topic.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
            else:
                content = st.session_state.prompt_engineer.generate_content(
                    content_type=content_type,
                    topic=topic,
                    context=None,
                    additional_requirements=additional_requirements if additional_requirements else None
                )
                
                st.subheader("Generated Content")
                st.markdown(content)
                
                st.download_button(
                    label="Download Content",
                    data=content,
                    file_name=f"{content_type}_{topic.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
    
    st.divider()
    st.markdown("**Educational Content Generator** - Uses RAG and prompt engineering to generate educational materials.")

if __name__ == "__main__":
    main()
