from typing import Tuple, Optional
def validate_match_result(your_goals, opponents_goals, result) -> Tuple[bool, Optional[str]]:
    if result == "Win":
        if int(your_goals) <= int(opponents_goals):
            return False, "Your goals can't be lower then opponent's goals when the result is a win."
        return True, None
    elif result == "Loss":
        if int(your_goals) >= int(opponents_goals):
            return False, "Your goals can't be greater then opponent's goals when the result is a loss."
        return True, None
    elif result == "Draw":
        if int(your_goals) != int(opponents_goals):
            return False, "Your goals can't be different from the opponent's goals when the result is a draw."
        return True, None
    return False, "Bro idk how you got here"
    
def validate_player_role(role, minutes_played, position):
    if role == "Starter":
        if int(minutes_played) < 1:
            return False, "A starter cannot play 0 minutes."
    elif role == "Substitute" and position == "Bench":
        if int(minutes_played) > 0:
            return False, "A substitute on the bench cannot play more then 0 minutes."
        
    return True, None

def validate_player_stats(max_goals_or_assists, goals, assists):
    if (int(goals)+int(assists)) > int(max_goals_or_assists):
        return False, "Goals and assists combined cannot be greater than total goals scored by your team."
    return True, None

def validate_player_discipline(yellow_cards, red_cards):
    if yellow_cards == 2:
        if red_cards != 1:
            return False, "A player cannot have 2 yellow cards but have 0 red cards."
        
    return True, None


def general_validation(match):
    result, error = validate_match_result(
        match["your_goals"],
        match["opponents_goals"],
        match["result"]
    )
    
    if not result:
        return result, error

    result, error = validate_player_role(
        match["role"],
        match["minutes"],
        match["position"]
    )
    
    if not result:
        return result, error

    result, error = validate_player_stats(
        match["your_goals"],
        match["goals"],
        match["assists"]
    )
    
    if not result:
        return result, error

    result, error = validate_player_discipline(
        match["yellow_cards"],
        match["red_cards"]
    )
    
    if not result:
        return result, error
    
    return True, None