#File Imports
from backend.database import init_database
from app.app_class import App
from app.app_state import AppState

#Flet Imports
import flet as ft

#RUN on iOS = flet run main.py --ios --name SoccerStatisticsTracker

#TODO:
# Learn PostgresSQL
# Learn paths and how to use terminal fr
# Learning ports, networking, traffic and hosting.
# Learn proper UX / GUI
# Learn Typescript / React OR Dart / Flutter for better frontent

#RUN PROGRAM / INIT --------------------

#Initalize the app and hand it off the App() class
def main(page: ft.Page) -> None:
    init_database()
    page.route = '/auth'
    page.title = "Soccer Statistics Tracker"
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    
    supabase = init_database()
    
    state = AppState(supabase = supabase)
    app = App(page,state)
    
    app.route_change()
     
if __name__ == "__main__":
    ft.run(main=main, assets_dir='assets')