from typing import Any
import asyncio
import flet as ft
from flet import View,Row, Column, Container, Text, Button, IconButton, AppBar, Divider, VerticalDivider
from flet import SafeArea, NavigationDrawer, NavigationDrawerDestination

#Universal Custom Controls (Appbar, Containers, Navigation Drawer)
@ft.control
class NavigationMenu(NavigationDrawer):
    def __init__(self) -> None:
        super().__init__(
            tile_padding=6,
            controls=[
                    Container(content=Text("Navigate", size=17, align=ft.Alignment.CENTER_LEFT, font_family='Chiron GoRound TC'), padding=ft.Padding.all(10),alignment=ft.Alignment.BOTTOM_CENTER),
                    ft.Divider(),
                    NavigationDrawerDestination(label='Home', icon=ft.Icons.HOME, selected_icon=ft.Icons.HOME_FILLED),
                    NavigationDrawerDestination(label='Add Match', icon=ft.Icons.CREATE_OUTLINED, selected_icon=ft.Icons.CREATE),
                    NavigationDrawerDestination(label='All Matches', icon=ft.Icons.LIST_OUTLINED, selected_icon=ft.Icons.LIST),
                    NavigationDrawerDestination(label='Specific Match', icon=ft.Icons.SEARCH_OUTLINED, selected_icon=ft.Icons.SEARCH),
                    NavigationDrawerDestination(label='Season Summary', icon=ft.Icons.STACKED_BAR_CHART_OUTLINED, selected_icon=ft.Icons.STACKED_BAR_CHART),
                    NavigationDrawerDestination(label='Edit Match', icon=ft.Icons.EDIT_OUTLINED, selected_icon=ft.Icons.EDIT),
                    NavigationDrawerDestination(label='Delete Match', icon=ft.Icons.DELETE_OUTLINED, selected_icon=ft.Icons.DELETE),
                ]
        )
    

@ft.control
class HomePageAppBar(AppBar):
    def __init__(self, page: ft.Page) -> None:
        self.app_page = page
        
        self.menu_button = IconButton(
                icon=ft.Icons.MENU, 
                hover_color=ft.Colors.GREY_300,
                on_click= self.show_drawer
            )
        
        super().__init__(
            leading= self.menu_button,
            title = Text(value="App",size=19),
            bgcolor = ft.Colors.GREY_200
        )
        
    async def show_drawer(self, e):
        await self.app_page.show_drawer()






#Homepage Screen
class HomePage():
    def __init__(self, page, state) -> None:
        self.page = page
        self.state = state
        self.view = View(
            drawer=NavigationMenu(),
            padding= ft.Padding.all(0),
            controls=[
                HomePageAppBar(page),
            ]
        )
    
#King of Data, main soure of app data
class AppState:
    #Anything can update this, since it passes into every view
    def __init__(self):
        self.match_data = []


#King Class, controls it all
class App():
    def __init__(self,page,state) -> None:
        self.page :ft.Page = page
        self.state = state
        self.HomePage = HomePage(page,state)
        
        self.page.on_route_change = self.route_change
        
    
    def route_change(self):
        self.page.views.clear()
        
        if self.page.route == '/':
            self.page.views.append(self.HomePage.view)
        
        self.page.update()


#Initalize the app and hand it off the App() class
def main(page: ft.Page) -> None:
    page.title = "Soccer Statistics Tracker"
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    
    state = AppState()
    app = App(page,state)
    
    app.route_change()
     
if __name__ == "__main__":
    ft.run(main=main)