#Control Imports
from frontend.controls.unique_controls import UniversalAppBar
#Flet Imports
import flet as ft
from flet import Text


#Error page, kinda obvious
class Error404_NotFound_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        self.view = ft.View(
            drawer=self.nav_menu,
            padding= ft.Padding.all(0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                UniversalAppBar(self.app_page),
                Text(value="Error 404: Page Not Found")
            ]
        )
