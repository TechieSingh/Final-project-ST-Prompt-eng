#!/usr/bin/env python3
"""
Simple CLI interface for Educational Content Generator
Run locally without Streamlit for quick testing
"""

import os
import sys
from dotenv import load_dotenv
from rag_system import RAGSystem
from prompt_engineer import PromptEngineer

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def main():
    """Main CLI interface"""
    print_header("Educational Content Generator - CLI")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        print("Please create a .env file with: OPENAI_API_KEY=your_key_here")
        sys.exit(1)
    
    print("✅ API Key loaded")
    
    # Initialize systems
    print("\n📚 Initializing RAG System and Prompt Engineer...")
    try:
        rag_system = RAGSystem(api_key=api_key)
        prompt_engineer = PromptEngineer(api_key=api_key)
        print("✅ Systems initialized successfully!\n")
    except Exception as e:
        print(f"❌ Error initializing systems: {str(e)}")
        sys.exit(1)
    
    # Main loop
    while True:
        print("\n" + "-"*60)
        print("What would you like to do?")
        print("1. Upload document to knowledge base")
        print("2. Generate content")
        print("3. Exit")
        print("-"*60)
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            # Upload document
            file_path = input("\nEnter path to PDF or TXT file: ").strip().strip('"')
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                continue
            
            try:
                print(f"\n📄 Loading document: {file_path}")
                documents = rag_system.load_document(file_path)
                print(f"✅ Loaded {len(documents)} document(s)")
                
                print("📝 Adding to knowledge base...")
                rag_system.add_documents(documents)
                print("✅ Document added to knowledge base!")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        elif choice == "2":
            # Generate content
            print("\n📝 Content Types:")
            print("1. Study Guide")
            print("2. Quiz")
            print("3. Explanation")
            print("4. Summary")
            print("5. Practice Problems")
            
            type_choice = input("\nSelect content type (1-5): ").strip()
            content_types = {
                "1": "study_guide",
                "2": "quiz",
                "3": "explanation",
                "4": "summary",
                "5": "practice_problems"
            }
            
            if type_choice not in content_types:
                print("❌ Invalid choice")
                continue
            
            content_type = content_types[type_choice]
            topic = input("\nEnter topic: ").strip()
            
            if not topic:
                print("❌ Topic cannot be empty")
                continue
            
            additional_requirements = input("\nAdditional requirements (optional, press Enter to skip): ").strip()
            if not additional_requirements:
                additional_requirements = None
            
            try:
                print(f"\n🤖 Generating {content_type.replace('_', ' ')} on '{topic}'...")
                print("⏳ This may take 10-30 seconds...\n")
                
                result = prompt_engineer.generate_with_rag(
                    content_type=content_type,
                    topic=topic,
                    rag_system=rag_system,
                    additional_requirements=additional_requirements
                )
                
                print_header(f"Generated {content_type.replace('_', ' ').title()}")
                print(result["content"])
                
                # Option to save
                save = input("\n💾 Save to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"{content_type}_{topic.replace(' ', '_')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Topic: {topic}\n")
                        f.write(f"Type: {content_type.replace('_', ' ').title()}\n")
                        f.write("="*60 + "\n\n")
                        f.write(result["content"])
                    print(f"✅ Saved to: {filename}")
                
            except Exception as e:
                print(f"❌ Error generating content: {str(e)}")
        
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        sys.exit(0)

