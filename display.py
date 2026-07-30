def display_all_matches(all_matches):
    if not all_matches:
        print("No data on previous games.")
        return
    i = 1
    for match in all_matches:
        print(f"""
-------------------------
Game {i}
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
        i += 1
    
    
def display_specific_match(all_matches, number):
    number -= 1
    if not all_matches:
        print("No data on previous matches.")
        return 
    
    stats = all_matches[number]
    
    if stats == None:
        print("Error.")
        return
    
    print(f"""
-------------------------
Game {number+1}
-------------------------

Opponent: {stats['opponent_name']}
Date: {stats['date']}
Competition: {stats['competition']}
Result: {stats['your_goals']}-{stats['opponents_goals']} ({stats['result']})

Position: {stats['position']}
Role: {stats['role']}

Performance 
Goals: {stats['goals']}
Assists: {stats['assists']}
Minutes Played: {stats['minutes']}
Confidence: {stats['confidence']}/10

Discipline 
Yellow Cards: {stats['yellow_cards']}
Red Cards: {stats['red_cards']}

Notes
{stats['notes']}
-------------------------
""")


def display_summary(summary):
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