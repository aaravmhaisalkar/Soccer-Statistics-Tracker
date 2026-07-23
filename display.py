def display_all_matches(all_matches):
    if all_matches == {}:
        print("No data on previous games.")
        return
    
    for match in all_matches:
        print(f"""
-------------------------
Game {match['id']}
-------------------------

Opponent: {match['opponent_name']}
Date: {match['date']}
Competition: {match['competition']}
Result: {match['your_goals']}-{match['opponents_goals']} ({match['result']})

Position: {match['position']}
Role: {match['role']}

Performance:
Goals: {match['goals']}
Assists: {match['assists']}
Minutes Played: {match['minutes']}
Confidence: {match['confidence']}/10

Discipline:
Yellow Cards: {match['yellow_cards']}
Red Cards: {match['red_cards']}

Notes:
{match['notes']}
-------------------------\n
        """)
    
    
def load_specific_match(all_matches, number):
    number -= 1
    if all_matches == {}:
        print("No data on previous matches.")
        return 
    
    stats = all_matches[number]
    
    if stats == None:
        print("Error.")
        return
    
    print(f"""
-------------------------
Game {stats['id']}
-------------------------

Opponent: {stats['opponent_name']}
Date: {stats['date']}
Competition: {stats['competition']}
Result: {stats['your_goals']}-{stats['opponents_goals']} ({stats['result']})

Position: {stats['position']}
Role: {stats['role']}

Performance -------------------
Goals: {stats['goals']}
Assists: {stats['assists']}
Minutes Played: {stats['minutes']}
Confidence: {stats['confidence']}/10

Discipline -------------------
Yellow Cards: {stats['yellow_cards']}
Red Cards: {stats['red_cards']}

Notes -------------------
{stats['notes']}
-------------------------
""")
