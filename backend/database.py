import sqlite3
from backend.validation import general_validation
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "match_data.db"

def init_database():
    with sqlite3.connect(DATABASE_PATH) as conn:    
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


def save_match(stats):
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:    
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
                    stats["notes"]
                )
            )
    
    except sqlite3.Error as e:
            return False, f"Database error: {e}"
    
    return True, None

def load_all_matches():
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches ORDER BY id")
            rows = cursor.fetchall()
            return True, rows
        
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
             
def delete_match(number):
    number -= 1
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
            match_to_be_deleted_ID = rows[number]['id']
            cursor.execute("DELETE FROM matches where id = ?", (match_to_be_deleted_ID,))
        
    
    except sqlite3.Error as e:
        return False, f"Database error: {e}"
    
    return True, None
                
def edit_match(number, updates):
    number -= 1 
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
            
            match_data = rows[number]
            match_ID = match_data['id']
            
            temp_updated_match = dict(match_data)
            
            for stat, value in updates.items():
                temp_updated_match[stat] = value
                
            validation_result, error = general_validation(temp_updated_match)
            
                
            if validation_result:
                for stat,value in updates.items():
                    cursor.execute(
                    f"UPDATE matches SET {stat} = ? WHERE id = ?", 
                    (value,match_ID))
            
            else:
                return False, f'Error: {error}'
    except sqlite3.Error as e:
        return f"Database error: {e}"         
        
    return True, None
  