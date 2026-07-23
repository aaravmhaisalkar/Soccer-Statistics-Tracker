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
        save_match(created_match)
        
    if response == "2":
        all_matches = load_all_matches()
        display_all_matches(all_matches)
    
    if response == "3":
        if len(load_all_matches()) == 0:
            print("Error: No matches found in data.")
            continue
        game_number = checking_input("What game number: ",0,len(load_all_matches()))
        all_matches = load_all_matches()
        load_specific_match(all_matches,game_number)
        
    if response == "4":
        all_matches = load_all_matches()
        summary = show_summary(all_matches)    
        print(
f'''
--- SUMMARY ---
Total Games Played: {summary['total_matches']}
Total Goals Scored: {summary['total_goals']}
Total Assists: {summary['total_assists']}
Total G/A: {summary['total_goals'] + summary['total_assists']}
Total Minutes Played: {summary['total_min_played']}
Total Yellow Cards: {summary['total_yellow_cards']}
Total Red Cards: {summary['total_red_cards']}
Average Confidence: {summary['average_confidence']:.2f}



Goals For (GF): {summary['goals_for']}
Goals Against (GA): {summary['goals_against']}
Goal Differential (GD): {summary['goal_differential']}
Record: {summary['wins']} W | {summary['draws']} D | {summary['losses']} L 
Win Percentage: {summary["win_percentage"]:.2f}%
'''
              )
    
    if response == "5":
        if len(load_all_matches()) == 0:
            print("Error: No matches found in data.")
            continue
        game_number = checking_input("What game number: ",1, len(load_all_matches()))
        delete_match(game_number)
        
    if response == "6":
        if len(load_all_matches()) == 0:
            print("Error: No matches found in data.")
            continue
        game_number = checking_input("What game number: ",1, len(load_all_matches()))
        stat_to_be_updated = checking_input_string(f'Which stat would you like to update for Game #{game_number}: ', "stats")

        current_data_rule = data_input_rules[f'{stat_to_be_updated}']
        
        if current_data_rule['type'] == "number":
            new_value = checking_input(f'Update {stat_to_be_updated} in Game #{game_number} to: ',current_data_rule['min'], current_data_rule['max'])
            
        elif current_data_rule['type'] == "string":
            new_value = checking_input_string(f'Update {stat_to_be_updated} in Game #{game_number} to: ', current_data_rule['category'])
        
        elif current_data_rule['type'] == "text":
            new_value = str(input(f'Update {stat_to_be_updated} in Game #{game_number} to: '))
        
    
        edit_match(game_number, stat_to_be_updated, new_value)
    
    if response == "7":
        flag = False
        break



