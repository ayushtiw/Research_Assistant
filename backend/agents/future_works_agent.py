from typing import List, Dict, Any
from datetime import datetime
from ..models.llm_manager import LLMManager

class FutureWorksAgent:
    def __init__(self, llm_manager: LLMManager, db_client):
        self.llm_manager = llm_manager
        self.db_client = db_client

    async def generate_review(self, topic: str) -> str:
        # Get papers for the topic from the last 5 years
        current_year = datetime.now().year
        papers = self.db_client.get_papers_by_topic(topic, current_year - 5, current_year)
        
        # Reduce context length by limiting the number of papers and abstract size
        papers = self._reduce_paper_context(papers)

        # Generate a single consolidated review prompt to save time and memory
        review = await self._generate_consolidated_review(topic, papers)
        
        return review

    async def _generate_consolidated_review(self, topic: str, papers: List[Dict[str, Any]]) -> str:
        prompt = f"""Write a concise research review on the topic '{topic}'.
Consider the following papers as reference:

{self._format_papers_for_prompt(papers)}

Focus on:
1. A brief introduction to the topic.
2. Major approaches and key findings.
3. Main challenges faced in the field.
4. Possible future research directions.

Review:"""
        
        return await self.llm_manager.generate_response(prompt)

    def _reduce_paper_context(self, papers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Limit to 2 papers to reduce context length and memory usage
        papers = papers[:2]
        
        # Reduce the length of abstracts to 200 characters for further optimization
        for paper in papers:
            if 'abstract' in paper and len(paper['abstract']) > 200:
                paper['abstract'] = paper['abstract'][:200] + '...'
        return papers

    def _format_papers_for_prompt(self, papers: List[Dict[str, Any]]) -> str:
        return "\n\n".join([
            f"Title: {paper['title']}\n"
            f"Authors: {', '.join(paper['authors'])}\n"
            f"Published: {paper['published_date'][:4]}\n"
            f"Abstract: {paper['abstract']}"
            for paper in papers
        ])
