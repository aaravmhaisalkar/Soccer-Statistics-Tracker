#Flet Imports
import flet as ft
from flet import View

#GUI Components - Flet
from gui_components.appbar import HomePageAppBar
from gui_components.navigation_bar import NavigationMenu
from gui_components.stat_widgets import StatRow

#Homepage Screen
class HomePage():
    def __init__(self, page, state) -> None:
        self.page = page
        self.state = state
        
        data_dict = [
            [self.state.all_matches_summary['wins'],'Wins'],
            [self.state.all_matches_summary['draws'],'Draws'],
            [self.state.all_matches_summary['losses'],'Losses']
        ]
        
        self.view = View(
            drawer=NavigationMenu(),
            padding= ft.Padding.all(0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                HomePageAppBar(page),
                StatRow(page,data_dict)
            ]
        )
    