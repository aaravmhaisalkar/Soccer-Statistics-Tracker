import asyncio
from supabase import AuthApiError, AuthError
import flet as ft


class Auth_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        
        self.sign_up_controls = {
            'email' : ft.TextField(
                label='Email'
            ),
            'password' : ft.TextField(
                label='Password',
                password=True
            ),
            'checkbox' : ft.Checkbox(
                label="Check for sign-up (NOT sign-in)"
            ),
        }

        
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
            padding= ft.Padding.all(16),
            bgcolor=ft.Colors.WHITE,
            controls= [
                ft.Container(
                    border=ft.Border.all(2, ft.Colors.BLACK),
                    border_radius=ft.BorderRadius.all(10), 
                    padding = ft.Padding.all(10),
                    content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                *self.sign_up_controls.values(),
                                ft.Button(
                                    content="Continue",
                                    on_click= lambda e: asyncio.create_task(self.check(e))
                                ),
                                self.error_bar
                            ]
                        )
                ),
                
                
            ]
        )
        
    async def check(self, e):
        checkbox = self.sign_up_controls.get('checkbox')
        email = self.sign_up_controls.get('email')
        password = self.sign_up_controls.get('password')
        
        if checkbox is not None and email is not None and password is not None:
            if checkbox.value:
                    sucess, result = self.state.sign_up_user(email=email.value,password=password.value)
                    
                    if not sucess:
                        self.error_bar.visible = True
                        self.error_bar.content = ft.Column(controls=[ft.Text("Error:"), ft.Text(str(result))], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        self.app_page.update()
                        
                        await asyncio.sleep(2)
                        
                        self.error_bar.visible = False
                        self.app_page.update()
                        return

                    
                    print('signing up...')
                    
                    await self.app_page.push_route("/home")
                              
            
            elif not checkbox.value:
                    sucess, result = self.state.sign_in_user(email=email.value,password=password.value)
                    
                    if not sucess:
                        self.error_bar.visible = True
                        self.error_bar.content = ft.Column(controls=[ft.Text("Error:"), ft.Text(str(result))], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                        self.app_page.update()
                        
                        await asyncio.sleep(2)
                        
                        self.error_bar.visible = False
                        self.app_page.update()
                        return

                    
                    print('logging in...')
                    
                    await self.app_page.push_route("/home")
                    

   