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
    # try:
    #     with open(FILE, "a") as file:
    #         file.write(json.dumps(stats)+"\n")
            
    # except FileNotFoundError:
    #     print("Error: The specified file 'data.txt' could not be found.")

    # except PermissionError:
    #     print("Error: You do not have permission to access this file.")

    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")

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
    # match_number = 0
    # matches = {}
    # try:
    #  with open(FILE, "r") as file:
    #     for line in file:
    #         match_number += 1
    #         match = json.loads(line)
    #         matches[f'Match {match_number}'] = match
            
    #     return matches
    
    # except FileNotFoundError:
    #     print("Error: The specified file 'matches.json' could not be found.")
    #     return {}

    # except PermissionError:
    #     print("Error: You do not have permission to access this file.")
    #     return {}

    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    #     return {}
          
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
    
    # number -= 1
    # try:
    #     with open(FILE, "r") as file:
    #         lines = file.readlines()
                
    #     with open(FILE, "w") as file:
    #         for index, line in enumerate(lines):
    #             if index != number:
    #                 file.write(line)
        
            
    # except FileNotFoundError:
    #     print("Error: The specified file 'matches.json' could not be found.")

    # except PermissionError:
    #     print("Error: You do not have permission to access this file.")

    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
                
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
        
    
    # stats = all_matches.get(f'Match {number}')
    
    # if stats == None:
    #     print("Error.")
    #     return
    
    # all_matches[f'Match {number}'][f'{stat}'] = update
        
    # try:       
    #     with open(FILE, "w") as file:     
    #         for _, match in all_matches.items():
    #             file.write(json.dumps(match)+'\n')
               
    # except FileNotFoundError:
    #     print("Error: The specified file 'matches.json' could not be found.")

    # except PermissionError:
    #     print("Error: You do not have permission to access this file.")

    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
  