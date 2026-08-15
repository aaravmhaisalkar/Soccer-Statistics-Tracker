from typing import Any
import flet as ft
from flet import Container, Text, NavigationDrawer, NavigationDrawerDestination


@ft.control
class NavigationMenu(NavigationDrawer):
    def __init__(self, page) -> None:
        self.app_page = page
                
        self.routes = {
            0 : '/',
            1 : '/add'
        }
        
        super().__init__(
            tile_padding=3,
            on_change = self.handle_change,
            controls=[
                    Container(
                        content=Text(
                            value="Navigate", 
                            size=17, 
                            align=ft.Alignment.CENTER_LEFT, 
                            font_family='Chiron GoRound TC',
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                        ), 
                        padding=ft.Padding.only(left=28, top=20, bottom=12),
                    ),
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
    
    async def handle_change(self,e: ft.Event[ft.NavigationDrawer]):
        route = self.routes.get(e.control.selected_index)
        
        if route:
            print(f'seleted: {route}')
            await self.page.push_route(route=route)

        else:
            print("yea fuck")
        
        await self.page.close_drawer()