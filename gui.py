#File Imports
from backend.database import init_database
from frontend.app.app_class import App
from frontend.app.app_state import AppState

#Flet Imports
import flet as ft

#RUN on iOS = flet run gui.py --ios --name SoccerStatisticsTracker

#RUN PROGRAM / INIT --------------------

#Initalize the app and hand it off the App() class
def main(page: ft.Page) -> None:
    init_database()
    page.route = '/home'
    page.title = "Soccer Statistics Tracker"
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    
    state = AppState()
    app = App(page,state)
    
    app.route_change()
     
if __name__ == "__main__":
    ft.run(main=main, assets_dir='assets')