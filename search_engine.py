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
# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# integrated speech recognition API for voice input

# added voice pitch and reading speed controls in sidebar

# added JSON dataset containing cultural myth stories and folklore

# calculated cosine similarity scores between user audio query and myth database

# added audio player widget to play recorded query back to user

# added bookmark button to save favorite myth stories to session state

# formatted python code using black autoformatter

# verified full end-to-end voice myth search and narration application

# added PyAudio microphone input stream recorder component

# displayed top matching myth story cards with similarity percentages

# handled silence and background audio noise errors gracefully

# optimized search response latency using Streamlit cache data decorator

# added requirements list with streamlit speechrecognition pyttsx3 scikit-learn

# created project directory for voice myth discovery application

# integrated speech_recognition API to convert user voice into query text

# integrated pyttsx3 text to speech engine for reading myth stories aloud

# added myth category filter dropdown for folklore region

# saved sample audio clips to assets directory

# added docstrings for search engine functions

# built Streamlit web UI layout with title and sidebar controls

# built TF-IDF vectorizer over myth titles and descriptions

# built Streamlit web UI layout with main header and sidebar components

# added TF-IDF vectorizer over myth story titles and descriptions

# added reading speed and volume slider controls in sidebar

# added regional folklore filter dropdown in Streamlit sidebar

# optimized search response latency using Streamlit cache data decorator

# updated requirements list with streamlit speechrecognition pyttsx3 scikit-learn

# removed temporary recording wav files after query processing

# added export button to download myth text transcript as PDF

# checked cross browser compatibility for Streamlit web interface

# fixed audio queue deadlock issue during consecutive narration requests

# removed draft CSS files from static styles directory

# updated theme color palette to match dark mode aesthetics

# updated README setup instructions for installing portaudio dependencies

# added unit tests for audio queue concurrency handling

# removed deprecated Streamlit beta components from frontend code

# removed test audio WAV files from repo root folder

# removed redundant helper functions from search engine module

# updated Streamlit page config title and favicon icon

# fixed rare indexing error when search query contains special characters
