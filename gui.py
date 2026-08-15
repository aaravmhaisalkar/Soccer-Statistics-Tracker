#Misc Imports 
from typing import Any
import asyncio
from backend.database import init_database

#File imports
from app_state import AppState
from router import Router
from gui_components.navigation_bar import NavigationMenu

#View Imports
from views.homepage import HomePage
from views.add_match import Add_Match

#Flet Imports
import flet as ft


class App():
    def __init__(self,page,state) -> None:
        self.page :ft.Page = page
        self.nav_menu = NavigationMenu(self.page)
        self.state = state
        
        self.general_controls = [self.page, self.state, self.nav_menu]
        
        self.page.on_route_change = self.route_change
    
    def route_change(self, e = None):
        self.page.views.clear()
        self.state.refresh()
        
        new_view = Router.get_views(self.page.route, self.general_controls)
        
        self.page.views.append(new_view)
        self.page.update()


#Initalize the app and hand it off the App() class
def main(page: ft.Page) -> None:
    init_database()
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