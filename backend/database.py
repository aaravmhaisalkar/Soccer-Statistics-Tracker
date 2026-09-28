import sqlite3
import os
from supabase import create_client, AuthApiError, AuthError
from backend.validation import general_validation
from pathlib import Path
from postgrest import APIError
from dotenv import load_dotenv


def init_database():
    load_dotenv()

    url = os.environ.get("URL")
    key = os.environ.get("KEY")

    if not url or not key:
        raise ValueError("Missing required environment variables: URL and KEY")

    return create_client(
        url, 
        key,
    )

def load_all_matches(supabase_client, user):
    try:
        full_data = supabase_client.table('Matches').select("*").eq("user_id", user.user.id).execute()
        match_data = full_data.data
        return True, match_data
    
    except (AuthError,AuthApiError, APIError, Exception) as error:
        return False, error

def save_match(supabase_client, user, stats):
    try:
        print(stats)
        response = supabase_client.table('Matches').insert({
            'user_id' : user.user.id,
            'opponent_name': stats['opponent_name'],
            'date': stats['date'],
            'competition': stats['competition'],
            'result': stats['result'],
            'role': stats['role'],
            'position': stats['position'],
            'goals': stats['goals'],
            'assists': stats['assists'],
            'minutes': stats['minutes'],
            'yellow_cards': stats['yellow_cards'],
            'red_cards': stats['red_cards'],
            'confidence': stats['confidence'],
            'your_goals': stats['your_goals'],
            'opponents_goals': stats['opponents_goals'],
            'notes': stats['notes'],
        }).execute()
        return True, response
    
    except (AuthError,AuthApiError, APIError, Exception) as error:
        print(f'{error}')
        return False, error
             
def delete_match(supabase_client, user, id):
    try:
        response = supabase_client.table('Matches').delete().eq("user_id", user.user.id).eq('id', id).execute()
        return True, response
        
    except (AuthError,AuthApiError, APIError, Exception) as error:
        return False, error

def edit_match(supabase_client, user, id, edited_match):
    try:
        validation_result, error = general_validation(edited_match)
        print(error)
    
        if validation_result:
            response = (
                supabase_client.table('Matches')
                .update({
                    'opponent_name': edited_match['opponent_name'],
                    'date': edited_match['date'],
                    'competition': edited_match['competition'],
                    'result': edited_match['result'],
                    'your_goals': edited_match['your_goals'],
                    'opponents_goals': edited_match['opponents_goals'],
                    'role': edited_match['role'],
                    'minutes': edited_match['minutes'],
                    'position': edited_match['position'],
                    'goals': edited_match['goals'],
                    'assists': edited_match['assists'],
                    'yellow_cards': edited_match['yellow_cards'],
                    'red_cards': edited_match['red_cards'],
                    'confidence': edited_match['confidence'],
                    'notes': edited_match['notes']
                })
                .eq('user_id', user.user.id)
                .eq('id', id)
                .execute()
            )
            
            
        else:
            return False, f'Error: {error}'
        
    
    except (AuthError,AuthApiError, APIError, Exception) as error:
        return False, error

    return True, None
  
def sign_up(supabase_client, email, password):
    try:
        response = supabase_client.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
        return True, response
                        
    except (AuthError,AuthApiError) as error:
        print(f'{error}')
        return False, error

def sign_in(supabase_client, email, password):
    try:
        response = supabase_client.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
        return True, response
                        
    except (AuthError,AuthApiError) as error:
        print(f'{error}')
        return False, error

def signout(supabase_client, user):
    try:
        if user:
            response = supabase_client.auth.sign_out()
                            
    except (AuthError,AuthApiError) as error:
        print(f'{error}')
        return False, error
    
    return True, None