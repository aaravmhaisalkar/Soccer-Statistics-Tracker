#File Imports
from frontend.router import Router
#Control Imports
from unique_controls import NavigationMenu
#Flet Imports
import flet as ft

#Main app class, honestly not that important feature-wise
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
        print('yea ok so we got this route:',self.page.route)
        new_view = Router.get_views(self.page.route, self.general_controls)
        self.page.views.append(new_view)
        self.page.update()
