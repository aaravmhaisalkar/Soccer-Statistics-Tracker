#Control Imports
from frontend.controls.unique_controls import UniversalAppBar, MatchDisplayTable_SMALL
#Flet Imports
import flet as ft
from flet import Row, Column, Container, Text

#Page for displaying all matches. Simpler data compared to specific match page.
class All_Matches_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        self.view = ft.View(
                    drawer=self.nav_menu,
                    padding= ft.Padding.all(0),
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        UniversalAppBar(self.app_page),
                        Container(
                            padding=ft.Padding.symmetric(horizontal=5),
                            content=Column(
                                controls = [
                                    Row(
                                        controls=[
                                            Text(value="All Matches", size=20)
                                        ], 
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    ft.Divider(),
                                ]
                            )
                        ),
                    ]
                )  
        
        
        self.all_matches = self.state.all_matches
        
        self.all_matches_datatable = MatchDisplayTable_SMALL(
            page=self.app_page,
            state=self.state,
            data=self.all_matches,
            nav_menu=self.nav_menu, 
            on_tap_function= self.navigate_to_full_data
        )
        
        errors = self.state.build_status_message()
        
        if errors != None:
            self.view.controls.append(errors)
            
        else:
            self.view.controls.extend([
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color=ft.Colors.GREY_600),
                        Text("For full match details, click on the game data row.", size=11, color=ft.Colors.GREY_600),
                    ]
                ),
                ft.Divider(),
                Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.all_matches_datatable],
                ),
                Row(
                    controls=[
                        ft.Icon(ft.Icons.SWIPE, size=17, color=ft.Colors.GREY_500),
                        ft.Text("Scroll for more", size=14, color=ft.Colors.GREY_500),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ])
        
    async def navigate_to_full_data(self,e, num):
        self.nav_menu.selected_index = 3
        self.state.all_match_selected_match_id = int(num)
        await self.app_page.push_route('/specific_match')
