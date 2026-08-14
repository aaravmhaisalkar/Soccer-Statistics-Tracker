#Misc Imports 
from typing import Any
import asyncio
from backend.database import init_database

#File imports
from app_state import AppState

#View Imports
from views.homepage import HomePage

#Flet Imports
import flet as ft
from flet import View,Row, Column, Container, Text, Button, IconButton, AppBar, Divider, VerticalDivider
from flet import SafeArea, NavigationDrawer, NavigationDrawerDestination

#GUI Components - Flet
from gui_components.appbar import HomePageAppBar
from gui_components.navigation_bar import NavigationMenu
from gui_components.stat_widgets import StatContainer,StatRow


class App():
    def __init__(self,page,state) -> None:
        self.page :ft.Page = page
        self.state = state
        
        #Using lambda for on-demand creation of the different Views
        #Good for updated data, without lambda the data is static and not dynamic like I need
        self.routes = {
            '/': lambda: HomePage(page,state).view
        }
        
        self.page.on_route_change = self.route_change
        
    
    def route_change(self, e = None):
        self.page.views.clear()
        self.state.refresh()
        #Gets route from self.routes dict, easier than 5+ if/else statements
        view_builder = self.routes.get(self.page.route)
        
        if view_builder:
            #Adds the views to the view stack
            #The () at the end of view_builder is to call the lambda function immediately
            self.page.views.append(view_builder())            
        
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