from datetime import datetime
from backend.rules import valid_results,valid_stats,valid_comps,valid_roles,valid_positions,data_input_rules

def checking_input_float(prompt, min_value, max_value):
    while True:
        try: 
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            print("Invalid input.")
        except ValueError:
            print("Invalid Input")

def checking_input(prompt, min_value, max_value):
    while True:
        try: 
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            print("Invalid input.")
        except ValueError:
            print("Invalid Input")

def checking_input_string(prompt, usage):
    paramaters = {}
    if usage == "result":
        paramaters = valid_results
        
    elif usage == "stats":
        paramaters = valid_stats
        
    elif usage == "competition":
        paramaters = valid_comps
        
    elif usage == "position":
        paramaters = valid_positions
        
    elif usage == "role":
        paramaters = valid_roles
    
    elif usage == "date":
        while True:
            try:
                date = str(input(prompt)).lower().strip()
                checked_date = datetime.strptime(date, "%m/%d/%Y").date()
                if checked_date < datetime.today().date():
                    return date
                else:
                    raise ValueError
                    
            except ValueError:
                try: 
                    checked_date = datetime.strptime(date, "%m-%d-%Y").date()
                    if checked_date < datetime.today().date():
                        return date
                    else:
                        raise ValueError
                                        
                except ValueError:
                    print("Invalid Input")
    
    while True:
        try: 
            value = str(input(prompt)).lower().strip()
            if value in paramaters:
                return paramaters[value]
            print("Invalid input.")
        except ValueError:
            print("Invalid Input")

