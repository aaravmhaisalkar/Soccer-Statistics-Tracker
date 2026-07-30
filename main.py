import json
from datetime import datetime
from database import *
from display import *
from input_validation import *
from rules import *
from stats import *
from match_creator import *

flag = True

init_database()

def handle_database_results(error):
    if isinstance(error, str):
        print(error)
        return False
    return True


while flag:
    print("""
1. Add match
2. View All Matches
3. View Specific Match
4. Show Summary
5. Delete Match
6. Edit Match Data
7. Exit
          """)
    response = input()
    
    if response == "1":
        created_match = create_match()
        error = save_match(created_match)
        if not handle_database_results(error):
            continue
        
        
    if response == "2":
        all_matches = load_all_matches()
        if not handle_database_results(all_matches):
            continue
        display_all_matches(all_matches)
        
        
    if response == "3":
        all_matches = load_all_matches()
        if not handle_database_results(all_matches):
            continue
        if len(all_matches) == 0:
            print("Error: No matches found in data.")
            continue
        game_number = checking_input("What game number: ",1,len(all_matches))
        all_matches = load_all_matches()
        if not handle_database_results(all_matches):
            continue
        display_specific_match(all_matches,game_number)
      
        
    if response == "4":
        all_matches = load_all_matches()
        if not handle_database_results(all_matches):
            continue
        summary = show_summary(all_matches)    
        display_summary(summary)
    
    
    if response == "5":
        all_matches = load_all_matches()
        if not handle_database_results(all_matches):
            continue
        if len(all_matches) == 0:
            print("Error: No matches found in data.")
            continue
        game_number = checking_input("What game number: ",1, len(all_matches))
        error = delete_match(game_number)
        if not handle_database_results(error):
            continue
        
        
    if response == "6":
        all_matches = load_all_matches()
        
        if not handle_database_results(all_matches):
            continue
        
        if len(all_matches) == 0:
            print("Error: No matches found in data.")
            continue
        
        game_number = checking_input("What game number: ",1,len(all_matches))
        stat_to_be_updated = checking_input_string(f'Which stat would you like to update for Game #{game_number}: ', "stats")

        if stat_to_be_updated in ("result", "opponents_goals", "your_goals"):
            updated_result = checking_input_string(f'Update result in Game #{game_number} to: ','resultk')
            updated_your_goals = checking_input(f'Update your goals in Game #{game_number} to: ',0,infinite_int)
            updated_opponent_goals = checking_input(f'Update opponents goals in Game #{game_number} to: ',0,infinite_int)
            
            updates = {
                'result':updated_result,
                'your_goals': updated_your_goals,
                "opponents_goals": updated_opponent_goals
            }                   
        
        else:
            current_data_rule = data_input_rules[f'{stat_to_be_updated}']
            
            
            
            if current_data_rule['type'] == "number":
                new_value = checking_input(f'Update {data_input_rules[f'{stat_to_be_updated}']['display_string']} in Game #{game_number} to: ',current_data_rule['min'], current_data_rule['max'])
                
            elif current_data_rule['type'] == "string":
                new_value = checking_input_string(f'Update {data_input_rules[f'{stat_to_be_updated}']['display_string']} in Game #{game_number} to: ', current_data_rule['category'])
            
            elif current_data_rule['type'] == "text":
                new_value = str(input(f'Update {data_input_rules[f'{stat_to_be_updated}']['display_string']} in Game #{game_number} to: '))
        
        
            updates = {
                f'{stat_to_be_updated}': new_value
            }
            
        error = edit_match(game_number, updates)
        
        
        if not handle_database_results(error):
            continue
 
               
    if response == "7":
        flag = False
        break



