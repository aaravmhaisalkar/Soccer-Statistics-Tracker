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
            tile_padding=3,
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
    
