from input_validation import *

infinite_int = 10**18

def create_match():
    #Match Data
    opponent_name = str(input("Versus: "))
    date = checking_input_string("Date of the match (MM/DD/YYYY): ", "date")
    competition = checking_input_string("What competition level was the match: ", "competition")
    result = checking_input_string("Win or loss: ", "results")
    
    #Player Data
    role = checking_input_string("Were you a starter or substitute: ", "role")
    position = checking_input_string("What position did you play this game: ", "position")
    goals = checking_input("Goals: ", 0, infinite_int)
    assists = checking_input("Assists: ", 0, infinite_int)
    minutes_played = checking_input("Minutes Played: ", 0, 120)
    yellow_cards = checking_input("How many yellow cards: ", 0, 2)
    if yellow_cards == 2:
        red_cards = 1
    else:
        red_cards = checking_input("How many red cards: ",0, 1)
    player_confidence = checking_input("How confident do you feel about the performance (0-10): ", 0, 10)

    your_goals = checking_input("How many goals did YOUR team score (GF):  ", 0, infinite_int)
    opponents_goals = checking_input("How many goals did the OPPONENT team score (GA): ", 0, infinite_int)
    
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
