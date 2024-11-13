from neo4j import GraphDatabase
from typing import List, Dict, Any

class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_paper(self, paper_data: Dict[str, Any]):
        with self.driver.session() as session:
            session.execute_write(self._create_paper, paper_data)

    @staticmethod
    def _create_paper(tx, paper_data):
        query = """
        CREATE (p:Paper {
            title: $title,
            authors: $authors,
            abstract: $abstract,
            published_date: $published_date,
            url: $url,
            topic: $topic
        })
        """
        tx.run(query, paper_data)

    def get_papers_by_topic(self, topic: str, start_year: int, end_year: int) -> List[Dict]:
        with self.driver.session() as session:
            return session.execute_read(self._get_papers_by_topic, topic, start_year, end_year)

    @staticmethod
    def _get_papers_by_topic(tx, topic: str, start_year: int, end_year: int):
        query = """
        MATCH (p:Paper)
        WHERE p.topic = $topic 
        AND datetime(p.published_date).year >= $start_year 
        AND datetime(p.published_date).year <= $end_year
        RETURN p
        ORDER BY p.published_date DESC
        """
        result = tx.run(query, topic=topic, start_year=start_year, end_year=end_year)
        return [dict(record["p"]) for record in result]

    def get_paper_by_title(self, title: str) -> Dict[str, Any]:
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Paper)
                WHERE p.title = $title
                RETURN p.title AS title, p.authors AS authors, p.abstract AS abstract, p.published_date AS published_date
            """, title=title)
            record = result.single()
            if record:
                return {
                    "title": record["title"],
                    "authors": record["authors"],
                    "abstract": record["abstract"],
                    "published_date": record["published_date"]
                }
            return None

    def get_related_papers(self, paper_id: str) -> List[Dict[str, Any]]:
        with self.driver.session() as session:
            return session.execute_read(self._get_related_papers, paper_id)

    @staticmethod
    def _get_related_papers(tx, paper_id: str):
        query = """
        MATCH (p:Paper {id: $paper_id})-[:RELATED_TO]->(related:Paper)
        RETURN related
        ORDER BY related.published_date DESC
        """
        result = tx.run(query, paper_id=paper_id)
        return [dict(record["related"]) for record in result]

    def update_paper_metadata(self, paper_id: str, metadata: Dict[str, Any]):
        with self.driver.session() as session:
            session.execute_write(self._update_paper_metadata, paper_id, metadata)

    @staticmethod
    def _update_paper_metadata(tx, paper_id: str, metadata: Dict[str, Any]):
        query = """
        MATCH (p:Paper {id: $paper_id})
        SET p += $metadata
        RETURN p
        """
        tx.run(query, paper_id=paper_id, metadata=metadata)

    # Optional: Close method if using 'with' context for Neo4j session
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
