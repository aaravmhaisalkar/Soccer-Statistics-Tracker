#Flet Imports
import flet as ft
from flet import View

#GUI Components - Flet
from gui_components.appbar import UniversalAppBar
from gui_components.navigation_bar import NavigationMenu
from gui_components.stat_widgets import StatRow

#Homepage Screen
class Add_Match():
    def __init__(self, page, state, nav_menu) -> None:
        self.page = page
        self.state = state
        self.nav_menu = nav_menu
        
        self.view = View(
            drawer=self.nav_menu,
            padding= ft.Padding.all(0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                UniversalAppBar(page=self.page)
            ]
        )
    