# Academic Research Paper Assistant

This application serves as a comprehensive research assistant that helps users search, analyze, and generate insights from academic papers. It uses multiple AI agents to provide features like paper search, question answering, and review generation.

## Features

- Search for research papers by topic and date range
- Interactive timeline visualization of papers
- Question answering system for paper analysis
- Automatic review paper generation
- Future research direction suggestions
- Paper relationship visualization

## Prerequisites

- Python 3.9+
- Neo4j Database
- Ollama
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd research_assistant
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and start Neo4j Desktop

5. Install and setup Ollama:
```bash
ollama pull mistral
```

6. Create `.env` file with required configurations

## Running the Application

1. Start Neo4j database

2. Start the backend server:
```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

3. Start the frontend:
```bash
cd frontend
streamlit run app.py
```

4. Access the application at `http://localhost:8501`

## Usage

1. Enter a research topic in the sidebar
2. Select date range for papers
3. View papers in the timeline
4. Ask questions about papers in the chat interface
5. Generate review papers using the review generator

## Project Structure

```
research_assistant/
├── backend/               # Backend services
│   ├── agents/           # AI agents
│   ├── database/         # Database operations
│   ├── models/           # LLM integration
│   └── api/              # FastAPI endpoints
├── frontend/             # Streamlit frontend
├── tests/                # Test cases
└── config.py            # Configuration
```


## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

