import sqlite3
import os
from supabase import create_client, AuthApiError, AuthError
from backend.validation import general_validation
from pathlib import Path
from postgrest import APIError
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

# def save_match(stats):
#     try:
#         with sqlite3.connect(DATABASE_PATH) as conn:    
#                 cursor = conn.cursor()    
#                 cursor.execute("""
#                 INSERT INTO matches (
#                 opponent_name,
#                 date,
#                 competition,
#                 result,
#                 role,
#                 position,
#                 goals ,
#                 assists ,
#                 minutes ,
#                 yellow_cards ,
#                 red_cards ,
#                 confidence ,
#                 your_goals ,
#                 opponents_goals ,
#                 notes)
#                 VALUES (?,?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                 """,
#                 (
#                     stats["opponent_name"],
#                     stats["date"],
#                     stats["competition"],
#                     stats["result"],
#                     stats["role"],
#                     stats["position"],
#                     stats["goals"] ,
#                     stats["assists"] ,
#                     stats["minutes"] ,
#                     stats["yellow_cards"] ,
#                     stats["red_cards"] ,
#                     stats["confidence"] ,
#                     stats["your_goals"] ,
#                     stats["opponents_goals"] ,
#                     stats["notes"]
#                 )
#             )
    
#     except sqlite3.Error as e:
#             return False, f"Database error: {e}"
    
#     return True, None

# def load_all_matches():
#     try:
#         with sqlite3.connect(DATABASE_PATH) as conn:
#             conn.row_factory = sqlite3.Row
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM matches ORDER BY id")
#             rows = cursor.fetchall()
#             return True, rows
        
#     except sqlite3.Error as e:
#         return False, f"Database error: {e}"
    
def load_all_matches(supabase_client, user):
    try:
        full_data = supabase_client.table('Matches').select("*").eq("user_id", user.user.id).execute()
        match_data = full_data.data
        return True, match_data
    
    except (AuthError,AuthApiError, APIError, Exception) as error:
        return False, error

def save_match(supabase_client, user, stats):
    try:
        print(stats)
        response = supabase_client.table('Matches').insert({
            'user_id' : user.user.id,
            'opponent_name': stats['opponent_name'],
            'date': stats['date'],
            'competition': stats['competition'],
            'result': stats['result'],
            'role': stats['role'],
            'position': stats['position'],
            'goals': stats['goals'],
            'assists': stats['assists'],
            'minutes': stats['minutes'],
            'yellow_cards': stats['yellow_cards'],
            'red_cards': stats['red_cards'],
            'confidence': stats['confidence'],
            'your_goals': stats['your_goals'],
            'opponents_goals': stats['opponents_goals'],
            'notes': stats['notes'],
        }).execute()
        return True, response
    
    except (AuthError,AuthApiError, APIError, Exception) as error:
        print(f'{error}')
        return False, error
             
# def delete_match(number):
#     number -= 1
#     try:
#         with sqlite3.connect(DATABASE_PATH) as conn:
#             conn.row_factory = sqlite3.Row
#             cursor = conn.cursor()
#             rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
#             match_to_be_deleted_ID = rows[number]['id']
#             cursor.execute("DELETE FROM matches where id = ?", (match_to_be_deleted_ID,))
        
    
#     except sqlite3.Error as e:
#         return False, f"Database error: {e}"
    
#     return True, None
      
def delete_match(supabase_client, user, id):
    try:
        response = supabase_client.table('Matches').delete().eq("user_id", user.user.id).eq('id', id).execute()
        return True, response
        
    except (AuthError,AuthApiError, APIError, Exception) as error:
        return False, error

          
# def edit_match(match_number, edited_match):
#     print(f'#{match_number} : edited - {edited_match}')
#     match_number -= 1 
#     try:
#         with sqlite3.connect(DATABASE_PATH) as conn:
#             conn.row_factory = sqlite3.Row
#             cursor = conn.cursor()
            
#             rows = cursor.execute("SELECT * FROM matches ORDER BY id").fetchall()
#             match_data = rows[match_number]
#             match_ID = match_data['id']
#             validation_result, error = general_validation(edited_match)
            
#             print(error)
#             if validation_result:
#                 for stat,value in edited_match.items():
#                     cursor.execute(
#                     f"UPDATE matches SET {stat} = ? WHERE id = ?", 
#                     (value,match_ID))
            
#             else:
#                 return False, f'Error: {error}'
            
#     except sqlite3.Error as e:
#         return f"Database error: {e}"         
        
#     return True, None

def edit_match(supabase_client, user, id, edited_match):
    try:
        validation_result, error = general_validation(edited_match)
        print(error)
    
        if validation_result:
            response = (
                supabase_client.table('Matches')
                .update({
                    'opponent_name': edited_match['opponent_name'],
                    'date': edited_match['date'],
                    'competition': edited_match['competition'],
                    'result': edited_match['result'],
                    'your_goals': edited_match['your_goals'],
                    'opponents_goals': edited_match['opponents_goals'],
                    'role': edited_match['role'],
                    'minutes': edited_match['minutes'],
                    'position': edited_match['position'],
                    'goals': edited_match['goals'],
                    'assists': edited_match['assists'],
                    'yellow_cards': edited_match['yellow_cards'],
                    'red_cards': edited_match['red_cards'],
                    'confidence': edited_match['confidence'],
                    'notes': edited_match['notes']
                })
                .eq('user_id', user.user.id)
                .eq('id', id)
                .execute()
            )
            
            
        else:
            return False, f'Error: {error}'
        
    
    except (AuthError,AuthApiError, APIError, Exception) as error:
        return False, error

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
        print(f'{error}')
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
        print(f'{error}')
        return False, error