import sqlite3
from .config import DB_PATH

def initialize_database(path=DB_PATH):
    """Creates the SQLite table with filepath tracking."""
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT,
                chunk_text TEXT
            )
        ''')
        conn.commit()

def insert_chunk(filepath: str, text: str, path=DB_PATH):
    """Inserts a single chunk and its origin file into the database."""
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO documents (filepath, chunk_text) VALUES (?, ?)', (filepath, text))
        conn.commit()

def get_chunks(id_list, db_path=DB_PATH):
    """Retrieves chunks by their IDs and formats them with their file paths."""
    if not id_list:
        return []
        
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        placeholders = ','.join(['?'] * len(id_list))
        query = f'SELECT id, filepath, chunk_text FROM documents WHERE id IN ({placeholders})'
        
        cursor.execute(query, id_list)
        results = cursor.fetchall()
        
    # Combine filepath and chunk text so Ollama knows exactly where the code came from
    chunk_dict = {row[0]: f"File: {row[1]}\nCode:\n{row[2]}" for row in results}
    
    # Return in the exact order of the similarity scores
    return [chunk_dict[i] for i in id_list if i in chunk_dict]