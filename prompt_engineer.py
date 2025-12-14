from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os


class PromptEngineer:
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            openai_api_key=api_key or os.getenv("OPENAI_API_KEY"),
            model_name=model,
            temperature=0.7
        )
        self.model = model
    
    def _get_base_system_prompt(self) -> str:
        return """You are an expert educational content creator. Generate high-quality, 
        accurate, and pedagogically sound educational materials. Always ensure that:
        1. Content is factually accurate
        2. Information is presented clearly and understandably
        3. Content is appropriate for the target audience
        4. Examples are relevant and helpful
        5. Content follows educational best practices"""
    
    def _get_content_type_prompts(self) -> Dict[str, str]:
        return {
            "study_guide": """Create a comprehensive study guide on the given topic. Include:
            - Key concepts and definitions
            - Important points to remember
            - Examples and applications
            - Common misconceptions to avoid
            - Study tips and strategies
            
            Format the content in a clear, organized manner with headings and bullet points.""",
            
            "quiz": """Generate a quiz on the given topic. Include:
            - Multiple choice questions (at least 5)
            - True/False questions (at least 3)
            - Short answer questions (at least 2)
            - Provide correct answers at the end
            
            Ensure questions test understanding, not just memorization.""",
            
            "explanation": """Provide a clear, detailed explanation of the given topic. Include:
            - Definition and overview
            - Key concepts explained simply
            - Real-world examples or applications
            - Step-by-step breakdown if applicable
            - Visual descriptions or analogies
            
            Make the explanation accessible to learners at different levels.""",
            
            "summary": """Create a concise summary of the given topic. Include:
            - Main points and key takeaways
            - Important facts or figures
            - Key relationships or connections
            - Brief conclusion
            
            Keep it concise but comprehensive.""",
            
            "practice_problems": """Generate practice problems on the given topic. Include:
            - Problems of varying difficulty (easy, medium, hard)
            - Step-by-step solutions
            - Explanations of solution methods
            - Tips for solving similar problems
            
            Ensure problems are practical and help build understanding."""
        }
    
    def generate_content(
        self,
        content_type: str,
        topic: str,
        context: Optional[str] = None,
        additional_requirements: Optional[str] = None
    ) -> str:
        system_prompt = self._get_base_system_prompt()
        
        content_prompts = self._get_content_type_prompts()
        if content_type not in content_prompts:
            content_type = "explanation"  # default fallback
        
        content_instruction = content_prompts[content_type]
        
        context_section = ""
        if context:
            context_section = f"\n\nRelevant Context from Knowledge Base:\n{context}\n\nUse this context to ensure accuracy and relevance. If the context doesn't fully cover the topic, supplement with your knowledge while maintaining accuracy."
        
        requirements_section = ""
        if additional_requirements:
            requirements_section = f"\n\nAdditional Requirements:\n{additional_requirements}"
        
        full_prompt = f"""{content_instruction}

Topic: {topic}{context_section}{requirements_section}

Generate the content now:"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=full_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"Error generating content: {str(e)}. Please check your API key and try again."
    
    def generate_with_rag(
        self,
        content_type: str,
        topic: str,
        rag_system,
        additional_requirements: Optional[str] = None
    ) -> Dict[str, str]:
        context = rag_system.get_context_string(topic, k=5)
        
        content = self.generate_content(
            content_type=content_type,
            topic=topic,
            context=context,
            additional_requirements=additional_requirements
        )
        
        return {
            "content": content,
            "context_used": context,
            "content_type": content_type,
            "topic": topic
        }
    
    def handle_edge_cases(self, user_input: str) -> Optional[str]:
        if not user_input or not user_input.strip():
            return "Please provide a topic or question."
        
        if len(user_input) > 2000:
            return "Input is too long. Please provide a more concise topic (under 2000 characters)."
        
        # basic content filter
        inappropriate_keywords = ["violence", "illegal", "harmful"]
        if any(keyword in user_input.lower() for keyword in inappropriate_keywords):
            return "Please ensure your topic is appropriate for educational content."
        
        return None
