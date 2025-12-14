# Educational Content Generator

A tool that creates educational content using RAG and prompt engineering. Built for a generative AI course project.

## What it does

This project generates different types of educational materials:
- Study guides
- Quiz questions
- Concept explanations
- Summaries
- Practice problems

## How it works

### RAG System
Uses ChromaDB to store and search through educational documents. When you ask for content on a topic, it finds relevant info from your knowledge base and uses that to generate more accurate content.

### Prompt Engineering
Different prompts for each content type. The system knows how to ask the AI to create a study guide vs a quiz, for example.

## Features

- Web interface (Streamlit)
- Upload your own documents to the knowledge base
- Generate different types of content
- Uses RAG to make content more accurate
- Download generated content

## Setup

### Requirements
- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone the repo:
```bash
git clone https://github.com/TechieSingh/Final-project-ST-Prompt-eng.git
cd Final-project-ST-Prompt-eng
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```

4. Initialize the knowledge base (adds some sample docs):
```bash
python setup_knowledge_base.py
```

5. Run the app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Project Structure

```
Final_Project/
├── app.py                      # Main app
├── rag_system.py              # RAG stuff
├── prompt_engineer.py         # Prompt handling
├── knowledge_base/            # Your documents go here
├── vector_store/             # Vector DB (auto-generated)
├── setup_knowledge_base.py   # Setup script
├── tests/                    # Tests
├── examples/                 # Example outputs
├── docs/                     # Documentation
└── web_page/                 # Web page
```

## Usage

1. Start the app: `streamlit run app.py`
2. Click "Initialize Systems" in the sidebar
3. (Optional) Upload documents to the knowledge base
4. Select content type
5. Enter your topic
6. Generate!

## Testing

Run the tests:
```bash
python tests/test_rag.py
python tests/test_prompts.py
```

## Documentation

Check the `docs/` folder for more details on architecture, implementation, and performance.

## Notes

- Generated content is marked as AI-generated
- Sources are tracked and can be cited
- Basic content filtering is implemented
- Privacy considerations for user data
