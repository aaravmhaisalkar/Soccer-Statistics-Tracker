#Control Imports
from frontend.controls.unique_controls import UniversalAppBar, MatchDisplayTable_SMALL
#Flet Imports
import flet as ft
from flet import Row, Column, Container, Text

class Delete_Match_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        self.seleted_match = ''

        self.all_matches = self.state.all_matches

        self.view = ft.View(
            drawer=self.nav_menu,
            padding=ft.Padding(0, 0, 0, 15),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                Row(
                    controls=[Text(value="Delete Match", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
            ]
        )

        errors = self.state.build_status_message()

        if errors != None:
            self.view.controls.append(errors)

        else:
            self.selection_table = Column(
                controls=[
                    MatchDisplayTable_SMALL(
                        page=self.app_page,
                        state=self.state,
                        data=self.all_matches,
                        nav_menu=self.nav_menu,
                        on_tap_function=self.selection_table_on_tap
                    )
                ]
            )

            self.confirmation_message = Container(
                visible=False,
                alignment=ft.Alignment.CENTER,
                width=350,
                padding=ft.Padding.all(15),
                border_radius=ft.BorderRadius.all(8),
                bgcolor=ft.Colors.RED_50,
                border=ft.Border.all(1, ft.Colors.RED_200),
            )

            self.view.controls.extend([
                Container(
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(horizontal=5),
                    content=Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.selection_table, self.confirmation_message]
                    )
                ),
            ])

    def selection_table_on_tap(self, e, num):
        self.seleted_match = num

        controls = Column(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                Row(
                    controls=[
                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.RED_700, size=20),
                        Text(
                            value=f'Delete Game #{self.seleted_match}? This cannot be undone.',
                            size=13,
                            color=ft.Colors.RED_900,
                        ),
                    ]
                ),
                Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(width=100, content="Cancel", on_click=self.disable_delete),
                        ft.Button(
                            width=100,
                            content="Delete",
                            on_click=self.delete_match,
                            bgcolor=ft.Colors.RED_600,
                            color=ft.Colors.WHITE,
                        ),
                    ]
                ),
            ]
        )

        self.confirmation_message.visible = True
        self.confirmation_message.content = controls
        self.app_page.update()

    def disable_delete(self, e=None):
        self.confirmation_message.visible = False
        self.confirmation_message.content = None
        self.app_page.update()
        self.seleted_match = ''

    async def delete_match(self, e=None):
        route = self.app_page.route
        result, error = self.state.delete_match(self.seleted_match)

        if result:
            self.seleted_match = ''
            self.disable_delete()
            #Ok so this looks janky icl, but best i couldve done for a actual reset. And i mean it works.
            await self.app_page.push_route('')
            await self.app_page.push_route(route)
        else:
            self.confirmation_message.content = Column(
                controls=[
                    Row(
                        controls=[
                            Text(f'Error: {error}'),
                            ft.Button(content="Close", on_click=self.disable_delete)
                        ]
                    )
                ]
            )
            self.app_page.update()
