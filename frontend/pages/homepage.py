#Control Imports
from frontend.controls.unique_controls import UniversalAppBar, StatRow
#Flet Imports
import flet as ft
from flet import Row, Text

#Homepage, i mean what else bro
class HomePage():
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
                        Row(
                            controls=[Text(value="Homepage", size=20)],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Divider(),
                    ]
                )
        
        errors = self.state.build_status_message()
                
        if errors != None:
            self.view.controls.append(errors)
            
        else:
            data_dict = [
                [self.state.all_matches_summary['wins'],'Wins'],
                [self.state.all_matches_summary['draws'],'Draws'],
                [self.state.all_matches_summary['losses'],'Losses']
            ]
            
            self.view.controls.append(StatRow(self.app_page,data_dict))
        
        