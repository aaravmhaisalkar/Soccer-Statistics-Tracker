def display_all_matches(all_matches):
    if all_matches == {}:
        print("No data on previous games.")
        return
    for match,stats in all_matches.items():
        print(f"""
-------------------------
Game {match}
-------------------------

Opponent: {stats['opponent_name']}
Date: {stats['date']}
Competition: {stats['competition']}
Result: {stats['your_goals']}-{stats['opponents_goals']} ({stats['result']})

Position: {stats['position']}
Role: {stats['role']}

Performance:
Goals: {stats['goals']}
Assists: {stats['assists']}
Minutes Played: {stats['minutes']}
Confidence: {stats['confidence']}/10

Discipline:
Yellow Cards: {stats['yellow_cards']}
Red Cards: {stats['red_cards']}

Notes:
{stats['notes']}
-------------------------\n
""")        

def load_specific_match(all_matches, number):
    if all_matches == {}:
        print("No data on previous matches.")
        return 
    
    stats = all_matches.get(f'Match {number}')
    
    if stats == None:
        print("Error.")
        return
    
    print(f"""
-------------------------
Game {number}
-------------------------

Opponent: {stats['opponent_name']}
Date: {stats['date']}
Competition: {stats['competition']}
Result: {stats['your_goals']}-{stats['opponents_goals']} ({stats['result']})

Position: {stats['position']}
Role: {stats['role']}

Performance:
Goals: {stats['goals']}
Assists: {stats['assists']}
Minutes Played: {stats['minutes']}
Confidence: {stats['confidence']}/10

Discipline:
Yellow Cards: {stats['yellow_cards']}
Red Cards: {stats['red_cards']}

Notes:
{stats['notes']}
-------------------------
""")
