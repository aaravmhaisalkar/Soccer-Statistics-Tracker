#Control Imports
from frontend.controls.unique_controls import UniversalAppBar, SeasonStatsDisplayTable
#Flet Imports
import flet as ft
from flet import Row, Column, Container, Text

#Shows season summary with simmilar style to all_matches / specific_match pages.
#No input/user stuff, just the data shown. no input really needed for this tbh idk how u would have it
class Season_Summary_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu

        self.view = ft.View(
            drawer=self.nav_menu,
            padding=ft.Padding(0, 0, 0, 10),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                Row(
                    controls=[Text(value="Season Stats Summary", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
            ]
        )

        errors = self.state.build_status_message()

        if errors != None:
            self.view.controls.append(errors)

        else:
            self.view.controls.append(
                Container(
                    padding=ft.Padding.symmetric(horizontal=5),
                    content=Column(
                        controls=[
                            SeasonStatsDisplayTable(page=self.app_page, data=self.state.all_matches_summary)
                        ]
                    )
                )
            )
