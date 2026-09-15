import sqlite3
import os
from supabase import create_client, AuthApiError, AuthError
from backend.validation import general_validation
from pathlib import Path
import supabase, supabase_auth
from dotenv import load_dotenv


def init_database():
    load_dotenv()

    url = os.environ.get("URL")
    key = os.environ.get("KEY")

    if not url or not key:
        raise ValueError("Missing required environment variables: URL and KEY")

    return create_client(
        url, 
        key,
    )


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "match_data.db"

# def init_database():
#     with sqlite3.connect(DATABASE_PATH) as conn:    
#         cursor = conn.cursor()    
#         cursor.execute("""CREATE TABLE IF NOT EXISTS matches(
#             id INTEGER PRIMARY KEY,
#             opponent_name TEXT,
#             date TEXT,
#             competition TEXT,
#             result TEXT,
#             role TEXT,
#             position TEXT,
#             goals INTEGER,
#             assists INTEGER,
#             minutes INTEGER,
#             yellow_cards INTEGER,
#             red_cards INTEGER,
#             confidence INTEGER,
#             your_goals INTEGER,
#             opponents_goals INTEGER,
#             notes TEXT
#             )
#             """)




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
                
def edit_match(match_number, edited_match):
    match_number -= 1 
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
            match_data = rows[match_number]
            match_ID = match_data['id']
            validation_result, error = general_validation(edited_match)
            
            print(error)
            if validation_result:
                for stat,value in edited_match.items():
                    cursor.execute(
                    f"UPDATE matches SET {stat} = ? WHERE id = ?", 
                    (value,match_ID))
            
            else:
                return False, f'Error: {error}'
            
    except sqlite3.Error as e:
        return f"Database error: {e}"         
        
    return True, None
  
def sign_up(supabase_client, email, password):
    try:
        response = supabase_client.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
        return True, response
                        
    except (AuthError,AuthApiError) as error:
        return False, error

def sign_in(supabase_client, email, password):
    try:
        response = supabase_client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
        return True, response
                        
    except (AuthError,AuthApiError) as error:
        return False, error