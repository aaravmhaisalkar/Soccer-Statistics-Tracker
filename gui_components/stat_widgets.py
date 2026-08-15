import flet as ft
from flet import Row, Column, Container, Text, VerticalDivider


@ft.control
class StatContainer(Container):
    def __init__(self, page: ft.Page, data) -> None:
        self.app_page = page
        self.number = data[0]
        self.stat = data[1]
        
        super().__init__(
            content=Column(
                spacing=1,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    Text(value=f"{self.number}", size=25),
                    Text(value=f"{self.stat}", size=17)
                ]
            )
        )


@ft.control
class StatRow(Container):
    def __init__(self, page: ft.Page, data_dict) -> None:
        self.app_page = page
        self.data_dict = data_dict
        
        controls = []
        
        for index, data in enumerate(self.data_dict):
            if index != (len(self.data_dict) - 1):
                controls.append(StatContainer(self.app_page, data))
                controls.append(VerticalDivider(width=3, color=ft.Colors.BLACK, leading_indent=10, trailing_indent=10))
            else:
                controls.append(StatContainer(self.app_page, data))

            
            
        super().__init__(
            height=100,
            width=350,
            border_radius=ft.BorderRadius.all(13),
            bgcolor=ft.Colors.GREY_300,
            content=Row(
                tight=True,
                spacing=35,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=controls
            )
        )

