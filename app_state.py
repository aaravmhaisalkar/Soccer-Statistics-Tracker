import json
from datetime import datetime
from backend.database import save_match,load_all_matches, delete_match, edit_match, init_database
from backend.display import display_all_matches,display_specific_match,display_summary
from backend.input_validation import checking_input,checking_input_float,checking_input_string
from backend.rules import data_input_rules,valid_comps,valid_positions,valid_results,valid_roles,valid_stats
from backend.stats import show_summary
from backend.match_creator import create_match


#Main soure of app data
#basically links the database/backend to the frontend/gui
class AppState:
    #Anything can update this, since it passes into every view
    def __init__(self):
        self.match_data = []
        self.all_matches_summary = {}

    def refresh(self):
        all_matches = load_all_matches()
        data = show_summary(all_matches=all_matches)
        
        self.all_matches_summary = data
        
        