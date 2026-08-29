from datetime import datetime
from backend.rules import valid_results,valid_stats,valid_comps,valid_roles,valid_positions, data_input_rules


def general_input_check(key, value):
    current_data_rule = data_input_rules.get(key)
    
    if not current_data_rule:
        return False, "Rule not found"
    
    if current_data_rule['type'] == "text":
        return True, value

    if value == '':
            return False, "All fields must be filled"
    
    if current_data_rule['type'] == "number":
        min_value = current_data_rule['min']
        max_value = current_data_rule['max']
        
        cleaned_value = float(value)
        if min_value <= cleaned_value <= max_value:
            return True, cleaned_value
        else:
            return False, f"Error with {current_data_rule['display_string']} value"
    
    elif current_data_rule['type'] == "name":
        cleaned_value = str(value).strip()
        if len(cleaned_value) < 1:
            return False, f"Error with {current_data_rule['display_string']}. Too short / No Value."
        else:
            return True, cleaned_value
        
    elif current_data_rule['type'] == "string":
        usage = current_data_rule['category']
        
        if usage == "date":
            date = str(value).lower().strip()
            checked_date = datetime.strptime(date, "%m/%d/%Y").date()
            if checked_date <= datetime.today().date():
                return True, date
            else:
                return False, f"Error with {current_data_rule['display_string']} value"
        
        parameters_map = {
            "result": valid_results, "stats": valid_stats,
            "competition": valid_comps, "position": valid_positions,
            "role": valid_roles
        }
        
        paramaters = parameters_map.get(usage, {})           
        cleaned_value = str(value).lower().strip()
        
        if cleaned_value in paramaters:
            return True, paramaters[cleaned_value]
        
        return False, f"Error with {current_data_rule['display_string']} value"
    
    return False, "Invalid Prompt"