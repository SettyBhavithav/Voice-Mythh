from typing import List, Dict
from myth_database import MythDatabase
from text_processor import TextProcessor

class SearchEngine:
    def __init__(self):
        """
        Initialize the SearchEngine with a database and text processor.
        """
        self.db = MythDatabase()
        self.text_processor = TextProcessor()

    def search(self, query: str) -> List[Dict]:
        """
        Search myths based on a query string.
        
        Args:
            query (str): The search query (e.g., keywords, places, characters).
        
        Returns:
            List[Dict]: A list of myth dictionaries ranked by relevance.
        """
        # Extract keywords from query
        query_keywords = self.text_processor.extract_keywords(query)
        query_keywords.append(query.strip())  # Include the full query as a keyword
        
        # Search in database
        results = self.db.search_myths(query_keywords)
        
        # Rank results by relevance
        for result in results:
            score = 0
            text_to_search = (
                result['original_text'] + ' ' +
                result['english_text'] + ' ' +
                result['summary'] + ' ' +
                ' '.join(result['keywords'])
            ).lower()
            for keyword in query_keywords:
                if keyword.lower() in text_to_search:
                    score += 1
            result['relevance_score'] = score
        
        # Sort by relevance score
        return sorted(results, key=lambda x: x['relevance_score'], reverse=True)

if __name__ == "__main__":
    # Example usage for testing
    se = SearchEngine()
    query = "hero village"
    results = se.search(query)
    for result in results:
        print(f"Relevance Score: {result['relevance_score']}, Place: {result['place']}, Summary: {result['summary']}")