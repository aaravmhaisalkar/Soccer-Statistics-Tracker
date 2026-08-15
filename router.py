#File imports
from app_state import AppState
from gui_components.navigation_bar import NavigationMenu

#View Imports
from views.homepage import HomePage
from views.add_match import Add_Match


#Flet Imports
import flet as ft

#TODO: ADD A ROUTE CLASS AND A VIEW BUILDER CLASS FOR FUTURE SIMPLICITY

class Router():
    @staticmethod
    def get_views(route, general_controls):
        match route:
            case '/':
                return HomePage(*general_controls).view
            case '/add':
                return Add_Match(*general_controls).view
            case _:
                return ft.View(controls=[ft.Text(value="404 Not Found")])