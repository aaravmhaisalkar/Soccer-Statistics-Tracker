import flet as ft
from flet import Text, IconButton, AppBar

@ft.control
class UniversalAppBar(AppBar):
    def __init__(self, page: ft.Page) -> None:
        self.app_page = page
        
        self.menu_button = IconButton(
                icon=ft.Icons.MENU, 
                hover_color=ft.Colors.GREY_300,
                on_click= self.show_drawer
            )
        
        super().__init__(
            leading= self.menu_button,
            title = Text(value="Soccer Statistics Tracker",size=19),
            bgcolor = ft.Colors.GREY_200
        )
        
    async def show_drawer(self, e):
        await self.app_page.show_drawer()
