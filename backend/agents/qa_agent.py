from typing import List, Dict, Any
from ..models.llm_manager import LLMManager

class QAAgent:
    def __init__(self, llm_manager: LLMManager, db_client):
        self.llm_manager = llm_manager
        self.db_client = db_client

    async def answer_question(self, question: str, paper_titles: List[str]) -> str:
        # Limit to top 3 papers to reduce processing time
        paper_titles = paper_titles[:3]
        papers = []
        for title in paper_titles:
            paper = self.db_client.get_paper_by_title(title)
            if paper:
                papers.append(paper)

        # Construct prompt and generate response
        prompt = self._construct_qa_prompt(question, papers)
        response = await self.llm_manager.generate_response(prompt)
        
        # Add citation metadata to the response
        response = self._add_citations(response, papers)
        return response

    def _construct_qa_prompt(self, question: str, papers: List[Dict[str, Any]]) -> str:
        context = "\n\n".join([
            f"Paper: {paper['title']}\n"
            f"Authors: {', '.join(paper['authors'])}\n"
            # Limit abstract length to 300 characters to optimize context size
            f"Abstract: {paper['abstract'][:300]}..." if len(paper['abstract']) > 300 else paper['abstract']
            for paper in papers
        ])
        
        prompt = f"""Based on the following research papers:

{context}

Question: {question}

Please provide a brief answer, citing specific papers if relevant.

Answer:"""
        
        return prompt

    def _add_citations(self, response: str, papers: List[Dict[str, Any]]) -> str:
        # Add paper references at the end of the response
        cited_papers = []
        for paper in papers:
            if paper['title'].lower() in response.lower():
                cited_papers.append(f"[{paper['title']}] - {', '.join(paper['authors'])} ({paper['published_date'][:4]})")
        
        if cited_papers:
            response += "\n\nReferences:\n" + "\n".join(cited_papers)
        
        return response
