infinite_int = 10**18

valid_results = {
    "w": "Win",
    "win": "Win",
    "wins": "Win",
    "won": "Win",
    "victory": "Win",
    "victories": "Win",

    "l": "Loss",
    "loss": "Loss",
    "losses": "Loss",
    "lose": "Loss",
    "loses": "Loss",
    "lost": "Loss",
    "defeat": "Loss",
    "defeated": "Loss",

    "d": "Draw",
    "draw": "Draw",
    "draws": "Draw",
    "drew": "Draw",
    "tie": "Draw",
    "tied": "Draw",
    "equal": "Draw",
}
valid_stats = {
# Goals
    "g": "goals",
    "goal": "goals",
    "goals": "goals",
    "gol": "goals",
    "goasl": "goals",
    "gaols": "goals",

    # Assists
    "a": "assists",
    "assist": "assists",
    "assists": "assists",
    "ast": "assists",
    "asts": "assists",
    "asist": "assists",
    "assissts": "assists",

    # Minutes
    "m": "minutes",
    "min": "minutes",
    "mins": "minutes",
    "minute": "minutes",
    "minutes": "minutes",
    "mnt": "minutes",
    "mnts": "minutes",
    "mins.": "minutes",
    "playing time": "minutes",
    "time": "minutes",

    # Confidence
    "c": "confidence",
    "conf": "confidence",
    "confidence": "confidence",
    "confidance": "confidence",
    "confidense": "confidence",
    "rating": "confidence",
    "performance rating": "confidence",

    # Result
    "r": "result",
    "res": "result",
    "result": "result",
    "outcome": "result",
    "score result": "result",

    # Opponent
    "opp": "opponent_name",
    "opponent": "opponent_name",
    "opponents": "opponent_name",
    "opponent name": "opponent_name",
    "team": "opponent_name",
    "versus": "opponent_name",
    "vs": "opponent_name",
    "enemy": "opponent_name",

    # Date
    "d": "date",
    "date": "date",
    "day": "date",
    "match date": "date",

    # Competition
    "comp": "competition",
    "competition": "competition",
    "league": "competition",
    "tournament": "competition",

    # Role
    "role": "role",
    "starter": "role",
    "start": "role",
    "sub": "role",
    "substitute": "role",
    "bench": "role",

    # Position
    "pos": "position",
    "position": "position",
    "place": "position",
    "spot": "position",

    # Yellow Cards
    "yc": "yellow_cards",
    "yellow": "yellow_cards",
    "yellow card": "yellow_cards",
    "yellow cards": "yellow_cards",
    "yellows": "yellow_cards",

    # Red Cards
    "rc": "red_cards",
    "red": "red_cards",
    "red card": "red_cards",
    "red cards": "red_cards",
    "reds": "red_cards",

    # Team Goals For
    "yg": "your_goals",
    "mygoals": "your_goals",
    "my_goals": "your_goals",
    "ourgoals": "your_goals",
    "our_goals": "your_goals",
    "yourgoals": "your_goals",
    "your_goals": "your_goals",
    "gf": "your_goals",
    "goals for": "your_goals",
    "team goals": "your_goals",

    # Opponent Goals Against
    "og": "opponents_goals",
    "oppgoals": "opponents_goals",
    "opponent_goals": "opponents_goals",
    "opponents_goals": "opponents_goals",
    "against": "opponents_goals",
    "ga": "opponents_goals",
    "goals against": "opponents_goals",
    "conceded": "opponents_goals",

    # Notes
    "n": "notes",
    "note": "notes",
    "notes": "notes",
    "comment": "notes",
    "comments": "notes",
    "description": "notes",
    "thoughts": "notes",
}
valid_comps = {
    # Friendlies
    "friendly": "Friendly",
    "friendlies": "Friendly",
    "scrimmage": "Friendly",
    "scrimmages": "Friendly",
    "exhibition": "Friendly",

    # General Tournaments
    "tournament": "Tournament",
    "tournaments": "Tournament",
    "tourney": "Tournament",
    "cup": "Tournament",

    # Recreational
    "rec": "Recreational",
    "recreation": "Recreational",
    "recreational": "Recreational",
    "rec soccer": "Recreational",

    # MLS NEXT
    "mls": "MLS NEXT",
    "mls next": "MLS NEXT",
    "mlsnext": "MLS NEXT",

    # National Academy League
    "nal": "National Academy League",
    "national academy league": "National Academy League",

    # Regional Academy League
    "ral": "Regional Academy League",
    "regional academy league": "Regional Academy League",

    # National League
    "national league": "National League",
    "nl": "National League",

    # National League Conferences
    "northeast conference": "National League Northeast Conference",
    "mid atlantic conference": "National League Mid Atlantic Conference",
    "midwest conference": "National League Midwest Conference",
    "frontier conference": "National League Frontier Conference",
    "pioneer conference": "National League Pioneer Conference",
    "pacific conference": "National League Pacific Conference",
    "sunshine conference": "National League Sunshine Conference",

    # National League Tiers
    "nl pro": "National League Pro",
    "national league pro": "National League Pro",

    "nl club": "National League Club",
    "national league club": "National League Club",

    # ECNL
    "ecnl": "ECNL",
    "elite clubs national league": "ECNL",

    # ECNL Regional League
    "ecnl rl": "ECNL Regional League",
    "ecnl regional league": "ECNL Regional League",
    "rl": "ECNL Regional League",

    # EDP
    "edp": "EDP",
    "edp league": "EDP",

    # ICSL
    "icsl": "ICSL",
    "inter county soccer league": "ICSL",

    # NCSL
    "ncsl": "NCSL",
    "national capital soccer league": "NCSL",

    # USYS State Cup
    "state cup": "State Cup",
    "statecup": "State Cup",

    # Presidents Cup
    "presidents cup": "Presidents Cup",
    "pres cup": "Presidents Cup",

    # USYS National Championships
    "nationals": "USYS National Championships",
    "national championships": "USYS National Championships",
    "usys nationals": "USYS National Championships",

    # US Club Soccer
    "us club": "US Club Soccer",
    "us club soccer": "US Club Soccer",

    # UPSL Youth
    "upsl": "UPSL Youth",
    "upsl youth": "UPSL Youth",

    # AYSO
    "ayso": "AYSO",

    # ODP
    "odp": "ODP",
    "olympic development program": "ODP",

    # High School
    "high school": "High School",
    "hs": "High School",
    "school": "High School",
}
valid_positions = {
    # Goalkeeper
    "gk": "Goalkeeper",
    "goalkeeper": "Goalkeeper",
    "keeper": "Goalkeeper",
    "goalie": "Goalkeeper",

    # Center Back
    "cb": "Center Back",
    "center back": "Center Back",
    "centre back": "Center Back",
    "central defender": "Center Back",

    # Left Back
    "lb": "Left Back",
    "left back": "Left Back",
    "left fullback": "Left Back",
    "left full back": "Left Back",

    # Right Back
    "rb": "Right Back",
    "right back": "Right Back",
    "right fullback": "Right Back",
    "right full back": "Right Back",

    # Fullback (General)
    "fb": "Fullback",
    "fullback": "Fullback",
    "full back": "Fullback",

    # Wing Back
    "lwb": "Left Wing Back",
    "left wing back": "Left Wing Back",
    "rwb": "Right Wing Back",
    "right wing back": "Right Wing Back",
    "wb": "Wing Back",
    "wing back": "Wing Back",

    # Defensive Midfielder
    "cdm": "Defensive Midfielder",
    "dm": "Defensive Midfielder",
    "defensive midfielder": "Defensive Midfielder",
    "holding midfielder": "Defensive Midfielder",
    "holding mid": "Defensive Midfielder",
    "6": "Defensive Midfielder",

    # Central Midfielder
    "cm": "Central Midfielder",
    "central midfielder": "Central Midfielder",
    "midfielder": "Central Midfielder",
    "mid": "Central Midfielder",
    "8": "Central Midfielder",

    # Attacking Midfielder
    "cam": "Attacking Midfielder",
    "am": "Attacking Midfielder",
    "attacking midfielder": "Attacking Midfielder",
    "10": "Attacking Midfielder",

    # Left Midfielder
    "lm": "Left Midfielder",
    "left midfielder": "Left Midfielder",

    # Right Midfielder
    "rm": "Right Midfielder",
    "right midfielder": "Right Midfielder",

    # Left Wing
    "lw": "Left Wing",
    "left wing": "Left Wing",
    "left winger": "Left Wing",

    # Right Wing
    "rw": "Right Wing",
    "right wing": "Right Wing",
    "right winger": "Right Wing",

    # General Winger
    "winger": "Winger",
    "wing": "Winger",
    "wings": "Winger",
    "w": "Winger",

    # Center Forward
    "cf": "Center Forward",
    "center forward": "Center Forward",
    "centre forward": "Center Forward",
    "false 9": "Center Forward",
    "false nine": "Center Forward",

    # Striker
    "st": "Striker",
    "striker": "Striker",
    "forward": "Striker",
    "9": "Striker",

    # Second Striker
    "ss": "Second Striker",
    "second striker": "Second Striker",
    "shadow striker": "Second Striker",

    # Sweeper
    "sw": "Sweeper",
    "sweeper": "Sweeper",

    #Other/Multiple
    "multiple": "Multiple Positions",
    "multi": "Multiple Positions",
    "various": "Multiple Positions",
    "rotated": "Multiple Positions",
}
valid_roles = {
    # Starter
    "starter": "Starter",
    "start": "Starter",
    "started": "Starter",
    "starting": "Starter",
    "starting 11": "Starter",
    "starting eleven": "Starter",
    "first team": "Starter",

    # Substitute
    "sub": "Substitute",
    "subs": "Substitute",
    "substitute": "Substitute",
    "substitutes": "Substitute",
    "bench": "Substitute",
    "benched": "Substitute",
    "reserve": "Substitute",
    "reserved": "Substitute",
    "came on": "Substitute",
    "off the bench": "Substitute",
}

data_input_rules = {
    "result": {
        "type": "string",
        "category": "result",
        "display_string": "result"
    },
    "confidence_level": {
        "type": "number",
        "min": 0,
        "max": 10,
        "display_string": "confidence"
    },
    "minutes_played": {
        "type": "number",
        "min": 0,
        "max": 120,
        "display_string": "minutes"
    },
    "date": {
        "type": "string",
        "category": "date",
        "display_string": "date"
    },
    "competition": {
        "type": "string",
        "category": "competition",
        "display_string": "competition"
    },
    "role": {
        "type": "string",
        "category": "role",
        "display_string": "role"
    },
    "position": {
        "type": "string",
        "category": "position",
        "display_string": "position"
    },
    "goals": {
        "type": "number",
        "min": 0,
        "max": infinite_int,
        "display_string": "goals"
    },
    "assists": {
        "type": "number",
        "min": 0,
        "max": infinite_int,
        "display_string": "assists"
    },
    "your_goals": {
        "type": "number",
        "min": 0,
        "max": infinite_int,
        "display_string": "your goals"
    },
    "opponents_goals": {
        "type": "number",
        "min": 0,
        "max": infinite_int,
        "display_string": "opponents goals"
    },
    "yellow_cards": {
        "type": "number",
        "min": 0,
        "max": 2,
        "display_string": "yellow cards"
    },
    "red_cards": {
        "type": "number",
        "min": 0,
        "max": 1,
        "display_string": "red cards"
    },
    "opponent_name": {
        "type": "text",
        "display_string": "opponent name"
    },
    "notes": {
        "type": "text",
        "display_string": "notes"
    },
}


