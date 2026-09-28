#Control Imports
from frontend.controls.universal_controls import UniversalDateInput,UniversalDropdownInput,UniversalFloatInputField,UniversalNumberInputField,UniversalTextInputField
from frontend.controls.unique_controls import UniversalAppBar, FormBuilder

#Flet Imports
import flet as ft
from flet import Row, Text

import asyncio

#Add Match Page
class Account_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        
        self.logout_button = ft.Button(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.LOGOUT, size=18),
                    ft.Text("Logout"),
                ],
                spacing=6,
            ),
            tooltip="Log out of your account",
            on_click=lambda e: asyncio.create_task(self.logout(e)),
        )
        
        self.error_bar = ft.Container(
            visible=False,
            width=300,
            height=95,
            bgcolor=ft.Colors.RED_200,
            border=ft.Border.all(1, ft.Colors.RED_500),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(10)
        )
        
        self.view = ft.View(
            drawer=self.nav_menu,
            padding= ft.Padding(2),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                Row(controls=[Text(value="Account", size=25)],alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                                controls=[
                                    Row(controls=[ft.Icon(icon=ft.Icons.ACCOUNT_CIRCLE_SHARP, size=65)],alignment=ft.MainAxisAlignment.CENTER),
                                    Row(controls=[Text(value=f'Email: {self.state.user.user.email}', size=18)],alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Divider(),
                                    Row(controls=[self.logout_button],alignment=ft.MainAxisAlignment.CENTER),
                                    Row(controls=[self.error_bar],alignment=ft.MainAxisAlignment.CENTER),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                    
                    border=ft.Border.all(3,ft.Colors.BLACK),
                    border_radius=ft.BorderRadius.all(10),
                    width=270,
                ),
                
            ]
        )
        
    async def logout(self, e):
        sucess, result = self.state.signout()
        print(result)
        if not sucess:
            self.error_bar.visible = True
            self.error_bar.content = ft.Column(controls=[ft.Text("Error:"), ft.Text(str(result))], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            self.app_page.update()
            
            await asyncio.sleep(2)
            
            self.error_bar.visible = False
            self.app_page.update()
            return

        
        print('signing out...')
        
        await self.app_page.push_route("/auth")
