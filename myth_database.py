import sqlite3
import json
import os
from typing import List, Dict

class MythDatabase:
    def __init__(self, db_path: str = "data/myths.db"):
        """
        Initialize the MythDatabase with a specified database path.
        
        Args:
            db_path (str): Path to the SQLite database file. Default is 'data/myths.db'.
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """
        Initialize the database with the myths table if it doesn't exist.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS myths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT NOT NULL,
                english_text TEXT,
                summary TEXT,
                keywords TEXT,
                language TEXT,
                place TEXT,
                region TEXT,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def insert_myth(self, myth_data: Dict) -> int:
        """
        Insert a new myth into the database.
        
        Args:
            myth_data (Dict): Dictionary containing myth details.
        
        Returns:
            int: The ID of the inserted myth.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO myths (original_text, english_text, summary, keywords, 
                             language, place, region, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            myth_data['original_text'],
            myth_data['english_text'],
            myth_data['summary'],
            json.dumps(myth_data['keywords']),
            myth_data['language'],
            myth_data.get('place', ''),
            myth_data.get('region', ''),
            myth_data.get('image_path', '')
        ))
        myth_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return myth_id
    
    def search_myths(self, query_keywords: List[str]) -> List[Dict]:
        """
        Search myths based on a list of keywords.
        
        Args:
            query_keywords (List[str]): List of keywords to search for.
        
        Returns:
            List[Dict]: List of matching myth dictionaries.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        search_conditions = []
        params = []
        for keyword in query_keywords:
            search_conditions.append('''
                (LOWER(original_text) LIKE ? OR 
                 LOWER(english_text) LIKE ? OR 
                 LOWER(summary) LIKE ? OR 
                 LOWER(keywords) LIKE ?)
            ''')
            params.extend([f'%{keyword.lower()}%'] * 4)
        query = f'''
            SELECT * FROM myths 
            WHERE {' OR '.join(search_conditions)}
            ORDER BY created_at DESC
        '''
        cursor.execute(query, params)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        for result in results:
            result['keywords'] = json.loads(result['keywords'])
        conn.close()
        return results
    
    def get_all_myths(self) -> List[Dict]:
        """
        Retrieve all myths from the database.
        
        Returns:
            List[Dict]: List of all myth dictionaries.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM myths ORDER BY created_at DESC')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        for result in results:
            result['keywords'] = json.loads(result['keywords'])
        conn.close()
        return results

if __name__ == "__main__":
    # Example usage for testing
    db = MythDatabase()
    sample_myth = {
        'original_text': 'A hero story.',
        'english_text': 'A hero story.',
        'summary': 'A hero fought.',
        'keywords': ['hero', 'fight'],
        'language': 'en',
        'place': 'Village',
        'region': 'Region',
        'image_path': ''
    }
    myth_id = db.insert_myth(sample_myth)
    print(f"Inserted myth with ID: {myth_id}")
    all_myths = db.get_all_myths()
    for myth in all_myths:
        print(f"ID: {myth['id']}, Place: {myth['place']}")