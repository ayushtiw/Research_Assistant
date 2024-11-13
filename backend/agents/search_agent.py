import arxiv
from typing import List, Dict, Any
from datetime import datetime

class SearchAgent:
    def __init__(self, db_client):
        self.db_client = db_client

    async def search(self, topic: str, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        # Search arXiv for papers
        search = arxiv.Search(
            query=topic,
            max_results=5,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        papers = []
        for result in search.results():
            # Convert to datetime for comparison
            paper_date = result.published.replace(tzinfo=None)
            if start_year <= paper_date.year <= end_year:
                paper_data = {
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "abstract": result.summary,
                    "published_date": paper_date.isoformat(),
                    "url": result.pdf_url,
                    "topic": topic
                }
                papers.append(paper_data)
                # Store in the Neo4j database
                self.db_client.add_paper(paper_data)

        return papers
