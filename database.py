import json

FILE = 'matches.json'

def save_match(stats):
    try:
        with open(FILE, "a") as file:
            file.write(json.dumps(stats)+"\n")
            
    except FileNotFoundError:
        print("Error: The specified file 'data.txt' could not be found.")

    except PermissionError:
        print("Error: You do not have permission to access this file.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def load_all_matches():
    match_number = 0
    matches = {}
    try:
     with open(FILE, "r") as file:
        for line in file:
            match_number += 1
            match = json.loads(line)
            matches[f'Match {match_number}'] = match
            
        return matches
    
    except FileNotFoundError:
        print("Error: The specified file 'matches.json' could not be found.")
        return {}

    except PermissionError:
        print("Error: You do not have permission to access this file.")
        return {}

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
          
def delete_match(number):
    number -= 1
    try:
        with open(FILE, "r") as file:
            lines = file.readlines()
                
        with open(FILE, "w") as file:
            for index, line in enumerate(lines):
                if index != number:
                    file.write(line)
        
            
    except FileNotFoundError:
        print("Error: The specified file 'matches.json' could not be found.")

    except PermissionError:
        print("Error: You do not have permission to access this file.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
                
def edit_match(number, stat, update):
    all_matches = load_all_matches()
    
    if all_matches == {}:
        print("No data on previous matches.")
        return 
    
    stats = all_matches.get(f'Match {number}')
    
    if stats == None:
        print("Error.")
        return
    
    all_matches[f'Match {number}'][f'{stat}'] = update
        
    try:       
        with open(FILE, "w") as file:     
            for _, match in all_matches.items():
                file.write(json.dumps(match)+'\n')
               
    except FileNotFoundError:
        print("Error: The specified file 'matches.json' could not be found.")

    except PermissionError:
        print("Error: You do not have permission to access this file.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
  