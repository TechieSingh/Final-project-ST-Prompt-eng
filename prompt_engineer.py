"""
Prompt Engineering Module

This module handles prompt creation and management for different content types.
It integrates with OpenAI's API to generate educational content using:
- Systematic prompting strategies
- Context management from RAG system
- Specialized prompts for different content types
- Edge case handling and validation
"""

from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os


class PromptEngineer:
    """
    Prompt engineering system for generating educational content.
    
    Manages prompt templates, context integration, and content generation
    using OpenAI's language models.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize Prompt Engineer with OpenAI API.
        
        Args:
            api_key: OpenAI API key (optional, can use env var)
            model: Model name to use (default: gpt-3.5-turbo)
        """
        self.llm = ChatOpenAI(
            openai_api_key=api_key or os.getenv("OPENAI_API_KEY"),
            model=model,
            temperature=0.7
        )
        self.model = model
    
    def _get_base_system_prompt(self) -> str:
        """
        Get base system prompt that defines the AI's role.
        
        Returns:
            Base system prompt string
        """
        return """You are an educational content creator. Generate accurate and clear educational materials. Make sure:
        1. Content is accurate
        2. Information is clear and easy to understand
        3. Content fits the target audience
        4. Examples are helpful
        5. Content is well-organized"""
    
    def _get_content_type_prompts(self) -> Dict[str, str]:
        """
        Get specialized prompts for different content types.
        
        Returns:
            Dictionary mapping content types to their prompt templates
        """
        return {
            "study_guide": """Create a study guide on the given topic. Include:
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
            
            Questions should test understanding, not just memorization.""",
            
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
            
            Keep it short but cover the main points.""",
            
            "practice_problems": """Generate practice problems on the given topic. Include:
            - Problems of varying difficulty (easy, medium, hard)
            - Step-by-step solutions
            - Explanations of solution methods
            - Tips for solving similar problems
            
            Problems should be practical and help build understanding."""
        }
    
    def generate_content(
        self,
        content_type: str,
        topic: str,
        context: Optional[str] = None,
        additional_requirements: Optional[str] = None
    ) -> str:
        """
        Generate educational content for a given topic.
        
        Args:
            content_type: Type of content (study_guide, quiz, explanation, etc.)
            topic: Topic or subject to generate content about
            context: Optional RAG context to include
            additional_requirements: Optional additional requirements from user
            
        Returns:
            Generated content as string, or error message if generation fails
        """
        system_prompt = self._get_base_system_prompt()
        
        content_prompts = self._get_content_type_prompts()
        if content_type not in content_prompts:
            content_type = "explanation"  # default fallback
        
        content_instruction = content_prompts[content_type]
        
        context_section = ""
        if context:
            context_section = f"\n\nRelevant Context from Knowledge Base:\n{context}\n\nUse this context to make the content accurate and relevant. If the context doesn't fully cover the topic, you can add your own knowledge but keep it accurate."
        
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
        """
        Generate content using RAG system to retrieve relevant context.
        
        Args:
            content_type: Type of content to generate
            topic: Topic or subject
            rag_system: RAGSystem instance to retrieve context
            additional_requirements: Optional additional requirements
            
        Returns:
            Dictionary with generated content, context used, content type, and topic
        """
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
        """
        Validate user input and handle edge cases.
        
        Checks for:
        - Empty or whitespace-only input
        - Input length exceeding limits
        - Inappropriate content
        
        Args:
            user_input: User's input string
            
        Returns:
            Error message string if validation fails, None if input is valid
        """
        if not user_input or not user_input.strip():
            return "Please provide a topic or question."
        
        if len(user_input) > 2000:
            return "Input is too long. Please provide a more concise topic (under 2000 characters)."
        
        # Basic content filter
        inappropriate_keywords = ["violence", "illegal", "harmful"]
        if any(keyword in user_input.lower() for keyword in inappropriate_keywords):
            return "Please make sure your topic is appropriate for educational content."
        
        return None
