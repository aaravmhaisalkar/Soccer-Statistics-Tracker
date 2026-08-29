#File imports
from backend.validation import general_validation
from backend.input_validation_v2 import general_input_check
from backend.display import display_all_matches
from backend.database import load_all_matches, save_match, delete_match, edit_match
from backend.stats import show_summary

#Flet Imports
import flet as ft
from flet import Text

#Main soure of app data
#basically links the database/backend to the frontend/gui
class AppState:
    #Anything can update this, since it passes into every view
    def __init__(self):
        #Good = good data, bad = error in data, empty = no data
        self.data_status = "" 
        self.all_match_selected_match_id = ''
        self.all_matches = {}
        self.all_matches_summary = {}

    def refresh(self):
        all_matches_check, all_matches = load_all_matches()
        
        if not all_matches_check:
            self.data_status = "bad"
            all_matches = {}
            return
    
        
        #We do this 'usable_all_matches' thing bc sqlite3 returns sqlite.Row objects not "good" data
        useable_data_check, usable_all_matches_data = display_all_matches(all_matches=all_matches)
        summery_check, summery_data = show_summary(all_matches=all_matches)
        
        if summery_check and useable_data_check:
            self.data_status = "good"
            self.all_matches_summary = summery_data
            self.all_matches = usable_all_matches_data
            return
        
        else:
            self.data_status = "empty"
            return
    
    def save_data(self,data_dict):
        #Validate Data
        errors = {}
        match = {}
        
        for field_name, value in data_dict.items():
            key = field_name.lower().replace(" ","_")
            result, value = general_input_check(key,value)
            if not result:
                errors[key] = value
            else:
                match[key] = value
        
        #Return if specific values are flawed
        if len(errors) > 0:
            print(errors)
            return False, errors
        
        validation_result, returned_value = general_validation(match)
        
        #Send Data to Database
        if not validation_result:
            errors["match"] = returned_value
            return False, errors
            
        result, error = save_match(match)
        
        if not result:
            errors["database"] = error
            return False, errors
        
        return True, None
    
    def delete_match(self, match_number):
        result, error = delete_match(match_number)
        if result:
            return True, None
        else:
            return False, error
        
    def edit_match(self, match_number, edited_match):
            result, error = edit_match(match_number=match_number, edited_match=edited_match)
            if result:
                return True, None
            else:
                return False, error
        
    def build_status_message(self):
        match self.data_status:
            case "bad":
                return Text("Something went wrong loading data.", color=ft.Colors.RED)
            case "empty":
                return Text("No matches yet — add your first one!")
            case _:
                return None
     