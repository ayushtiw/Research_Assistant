from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
import uvicorn
from config import Config

# Import necessary modules
from backend.agents.search_agent import SearchAgent
from backend.agents.qa_agent import QAAgent
from backend.agents.future_works_agent import FutureWorksAgent
from backend.database.neo4j_client import Neo4jClient
from backend.models.llm_manager import LLMManager

# Create a FastAPI app instance
app = FastAPI()

# Initialize Neo4j client
db_client = Neo4jClient(Config.NEO4J_URI, Config.NEO4J_USER, Config.NEO4J_PASSWORD)

# Initialize LLM manager
llm_manager = LLMManager(Config.MODEL_NAME)

# Initialize Agents
search_agent = SearchAgent(db_client)
qa_agent = QAAgent(llm_manager, db_client)
future_works_agent = FutureWorksAgent(llm_manager, db_client)

# Define the request models
class PaperRequest(BaseModel):
    topic: str
    start_year: Optional[int] = None
    end_year: Optional[int] = None

class Question(BaseModel):
    text: str
    papers: List[str]  # List of paper IDs or titles

# API endpoint to search for papers
@app.post("/search_papers")
async def search_papers(request: PaperRequest):
    try:
        # Use the search agent to find papers on a topic
        papers = await search_agent.search(
            request.topic,
            request.start_year or datetime.now().year - 5,
            request.end_year or datetime.now().year
        )
        return {"papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to ask a question about papers
@app.post("/ask_question")
async def ask_question(question: Question):
    try:
        # Use the QA agent to answer the question
        answer = await qa_agent.answer_question(question.text, question.papers)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to generate a research review
@app.post("/generate_review")
async def generate_review(request: PaperRequest):
    try:
        # Use the future works agent to generate a review
        review = await future_works_agent.generate_review(request.topic)
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API using Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)
