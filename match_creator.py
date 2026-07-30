from input_validation import checking_input,checking_input_float,checking_input_string
from validation import validate_match_result,validate_player_discipline,validate_player_role,validate_player_stats

infinite_int = 10**18

def create_match():
    #Match Data
    opponent_name = str(input("Versus: "))
    date = checking_input_string("Date of the match (MM/DD/YYYY): ", "date")
    competition = checking_input_string("What competition level was the match: ", "competition")
    
    #Result --------------------
    while True:
        result = checking_input_string("Win/Loss/Draw: ", "result")
        your_goals = checking_input("How many goals did YOUR team score (GF):  ", 0, infinite_int)
        opponents_goals = checking_input("How many goals did the OPPONENT team score (GA): ", 0, infinite_int)
        
        valid, error_message = validate_match_result(your_goals, opponents_goals, result)
        
        if valid:
            break
        
        print(error_message)
        
    #Player Role/Minutes/Position --------------------
    while True:
        role = checking_input_string("Were you a starter or substitute: ", "role")
        minutes_played = checking_input("Minutes Played: ", 0, 120)
        
        if minutes_played == 0:
            position = "Bench"
            goals = assists = yellow_cards = red_cards = 0
            
        else:
            position = checking_input_string("What position did you play this game: ", "position")
                  
        valid, error_message = validate_player_role(role,minutes_played,position)  
        
        if valid:
            break
        
        print(error_message)
    
    #Player Match Stats --------------------
    if minutes_played > 0:
        while True:
            max_goals_or_assists = your_goals
            goals = checking_input("Goals: ", 0, max_goals_or_assists)
            assists = checking_input("Assists: ", 0, max_goals_or_assists)
            
            valid, error_message = validate_player_stats(max_goals_or_assists, goals, assists)
                    
            if valid:
                break
            
            print(error_message)
        
        #Player Discipline --------------------
        while True:
            yellow_cards = checking_input("How many yellow cards: ", 0, 2)
            red_cards = checking_input("How many red cards: ",0, 1)
                
            valid, error_message = validate_player_discipline(yellow_cards,red_cards)
                            
            if valid:
                break
            
            print(error_message)
                    
    player_confidence = checking_input_float("How confident do you feel about the performance (0-10): ", 0, 10)

    notes = str(input("Any notes for this match? (ex. 'No goals, but played well'): "))

    stats = {
        # Match Info
        "opponent_name": opponent_name,
        "date": date,
        "competition": competition,
        "result": result,

        # Player Context
        "role": role,
        "position": position,

        # Player Performance
        "goals": goals,
        "assists": assists,
        "minutes": minutes_played,
        "confidence": player_confidence,

        # Match Discipline
        "yellow_cards": yellow_cards,
        "red_cards": red_cards,

        # Team Result
        "your_goals": your_goals,
        "opponents_goals": opponents_goals,

        # Notes
        "notes": notes
    }
    
    return stats

