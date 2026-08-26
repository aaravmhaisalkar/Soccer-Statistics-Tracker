def show_summary(all_matches):
    
    if not all_matches:
        return False, "empty"
    
    total_matches = len(all_matches)
    total_goals = 0
    total_min_played = 0
    total_assists = 0
    total_confidence = 0
    total_yellow_cards = 0
    total_red_cards = 0
    wins = 0
    draws = 0
    losses = 0
    goals_for = 0
    goals_against= 0
    

    for stats in all_matches:
        total_goals += stats['goals']
        total_assists += stats['assists']
        total_confidence += stats['confidence']
        total_yellow_cards += stats['yellow_cards']
        total_red_cards += stats['red_cards']
        total_min_played += stats['minutes']
        goals_for += stats['your_goals']
        goals_against += stats['opponents_goals']
        
        if stats['result'].lower() == "win":
            wins += 1
        elif stats['result'].lower() == 'loss':
            losses += 1
        elif stats['result'].lower() == 'draw': 
            draws += 1
            
    average_confidence = total_confidence / total_matches
    win_percentage = (wins/total_matches)*100
    goal_differential = goals_for - goals_against
        
    return True, {
        "total_yellow_cards": total_yellow_cards,
        "total_red_cards": total_red_cards,
        "total_matches": total_matches,
        "total_goals": total_goals,
        "total_min_played": total_min_played,
        "total_assists": total_assists,
        "average_confidence": average_confidence,
        "wins": wins,
        "win_percentage": win_percentage,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goal_differential": goal_differential
    } 
                      
           