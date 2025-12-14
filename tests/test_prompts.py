import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompt_engineer import PromptEngineer
from dotenv import load_dotenv

load_dotenv()

def test_prompt_initialization():
    print("Testing prompt engineer initialization...")
    pe = PromptEngineer(api_key=os.getenv("OPENAI_API_KEY"))
    assert pe.llm is not None
    print("Prompt engineer initialized successfully")

def test_edge_case_handling():
    print("Testing edge case handling...")
    pe = PromptEngineer(api_key=os.getenv("OPENAI_API_KEY"))
    
    result = pe.handle_edge_cases("")
    assert result is not None
    print("Empty input handled correctly")
    
    long_input = "a" * 3000
    result = pe.handle_edge_cases(long_input)
    assert result is not None
    print("Long input handled correctly")
    
    result = pe.handle_edge_cases("Normal topic")
    assert result is None
    print("Normal input accepted")

def test_content_type_prompts():
    print("Testing content type prompts...")
    pe = PromptEngineer(api_key=os.getenv("OPENAI_API_KEY"))
    
    content_types = ["study_guide", "quiz", "explanation", "summary", "practice_problems"]
    prompts = pe._get_content_type_prompts()
    
    for ct in content_types:
        assert ct in prompts
        print(f"Prompt for '{ct}' exists")

if __name__ == "__main__":
    print("Running prompt engineering tests...\n")
    
    try:
        test_prompt_initialization()
        test_edge_case_handling()
        test_content_type_prompts()
        print("\nAll prompt engineering tests passed!")
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        import traceback
        traceback.print_exc()
