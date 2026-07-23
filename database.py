import json
import sqlite3

def init_database():
    with sqlite3.connect('match_data.db') as conn:    
        cursor = conn.cursor()    
        cursor.execute("""CREATE TABLE IF NOT EXISTS matches(
            id INTEGER PRIMARY KEY,
            opponent_name TEXT,
            date TEXT,
            competition TEXT,
            result TEXT,
            role TEXT,
            position TEXT,
            goals INTEGER,
            assists INTEGER,
            minutes INTEGER,
            yellow_cards INTEGER,
            red_cards INTEGER,
            confidence INTEGER,
            your_goals INTEGER,
            opponents_goals INTEGER,
            notes TEXT
            )
            """)

      
FILE = 'matches.json'

def save_match(stats):
    try:
        with sqlite3.connect('match_data.db') as conn:    
                cursor = conn.cursor()    
                cursor.execute("""
                INSERT INTO matches (
                opponent_name,
                date,
                competition,
                result,
                role,
                position,
                goals ,
                assists ,
                minutes ,
                yellow_cards ,
                red_cards ,
                confidence ,
                your_goals ,
                opponents_goals ,
                notes)
            VALUES (?,?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
            stats["opponent_name"],
            stats["date"],
            stats["competition"],
            stats["result"],
            stats["role"],
            stats["position"],
            stats["goals"] ,
            stats["assists"] ,
            stats["minutes"] ,
            stats["yellow_cards"] ,
            stats["red_cards"] ,
            stats["confidence"] ,
            stats["your_goals"] ,
            stats["opponents_goals"] ,
            stats["notes"])
                )
    except sqlite3.Error as e:
        print(f'Database error: {e}')

def load_all_matches():
    try:
        with sqlite3.connect('match_data.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches ORDER BY id")
            rows = cursor.fetchall()
            
            return rows
        
    except sqlite3.Error as e:
        print(f'Database error: {e}')       
          
def delete_match(number):
    number -= 1
    try:
        with sqlite3.connect('match_data.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
            match_to_be_deleted_ID = rows[number]['id']
            cursor.execute("DELETE FROM matches where id = ?", (match_to_be_deleted_ID,))
            
    except sqlite3.Error as e:
        print(f'Database error: {e}')
                
def edit_match(number, stat, update):
    number -= 1 
    all_matches = load_all_matches()
    
    if all_matches == []:
        print("No data on previous matches.")
        return
    try:
        with sqlite3.connect('match_data.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
            match_to_be_updated_ID = rows[number]['id']
            cursor.execute(
                f"UPDATE matches SET {stat} = ? WHERE id = ?", 
                (update,match_to_be_updated_ID))
            
    except sqlite3.Error as e:
        print(f'Database error: {e}')         
        
  