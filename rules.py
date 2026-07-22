infinite_int = 10**18
data_input_rules= {
    "result": {
        "type" : "string",
        "category" : "result"
    },
    "confidence": {
        "type" : "number",
        "min" : 0,
        "max" : 10
    },
    "minutes": {
        "type" : "number",
        "min" : 0,
        "max" : 120
    },
    "date": {
        "type" : "string",
        "category" : "date"
    },
    "competition": {
        "type" : "string",
        "category" : "competition"
    },
    "role": {
        "type" : "string",
        "category" : "role"
    },
    "position": {
        "type" : "string",
        "category" : "position"
    },
    "goals": {
        "type" : "number",
        "min" : 0,
        "max" : infinite_int 
    },
    "assists": {
        "type" : "number",
        "min" : 0,
        "max" : infinite_int 
    },
    "your_goals": {
        "type" : "number",
        "min" : 0,
        "max" : infinite_int 
    },
    "opponents_goals": {
        "type" : "number",
        "min" : 0,
        "max" : infinite_int 
    },
    "yellow_cards": {
        "type" : "number",
        "min" : 0,
        "max" : 2 
    },
    "red_cards": {
        "type" : "number",
        "min" : 0,
        "max" : 1 
    },
    "opponent_name": {
        "type" : "text",
    },
    "notes": {
        "type" : "text",
    },
}