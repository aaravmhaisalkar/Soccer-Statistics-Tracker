#Control Imports
from frontend.controls.universal_controls import UniversalNumberInputField
from frontend.controls.unique_controls import UniversalAppBar, MatchDisplayTable_FULL
#Flet Imports
import flet as ft
from flet import Row, Column, Container, Text

#Page for displaying all matches. Simpler data compared to specific match page.
class Specific_Match_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu

        self.all_matches = self.state.all_matches

        self.view = ft.View(
            drawer=self.nav_menu,
            padding=ft.Padding.all(0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                Row(
                    controls=[Text(value="Specific Match Data", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
            ]
        )

        errors = self.state.build_status_message()

        if errors != None:
            self.view.controls.append(errors)

        else:
            self.match_number_input = UniversalNumberInputField(
                page=self.app_page,
                label="Match Number",
                lower_bound=1,
                upper_bound=len(self.all_matches),
            )

            self.match_data_contianer = Container(
                disabled=True,
            )

            self.view.controls.append(
                Container(
                    padding=ft.Padding.symmetric(horizontal=5),
                    content=Column(
                        controls=[
                            Row(
                                controls=[
                                    self.match_number_input,
                                    ft.Button(content="ok", on_click=self.on_click)
                                ]
                            ),
                            self.match_data_contianer,
                        ]
                    )
                )
            )

            if isinstance(self.state.all_match_selected_match_id, int):
                id = int(self.state.all_match_selected_match_id)
                specific_match_data = self.all_matches[id]
                self.state.all_match_selected_match_id = ''
                self.match_number_input.value = str(id)
                self.match_data_contianer.content = MatchDisplayTable_FULL(page=self.app_page, data=specific_match_data, number=id)

    def on_click(self, e):
        value = self.match_number_input.value

        if value != "" and int(value) <= int(len(self.all_matches)):
            specific_match_data = self.all_matches[int(value)]
            self.match_data_contianer.disabled = False
            self.match_data_contianer.content = MatchDisplayTable_FULL(page=self.app_page, data=specific_match_data, number=value)

        self.app_page.update()
