#Misc Imports 
import asyncio


#Control Imports
from frontend.controls.universal_controls import UniversalDateInput,UniversalDropdownInput,UniversalFloatInputField,UniversalNumberInputField,UniversalTextInputField
from frontend.controls.unique_controls import UniversalAppBar, FormBuilder, MatchDisplayTable_SMALL
#Flet Imports
import flet as ft
from flet import Row, Column, Container, Text

class Edit_Match_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        self.seleted_match = ''
        self.form_builder :FormBuilder | str  = ''
        self.all_matches = self.state.all_matches

        
        self.view = ft.View(
            drawer=self.nav_menu,
            padding=ft.Padding(0, 0, 0, 15),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                Row(
                    controls=[Text(value="Edit Match", size=20)],
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
                bgcolor=ft.Colors.LIGHT_GREEN_50,
                border=ft.Border.all(1, ft.Colors.LIGHT_GREEN_200),
            )

            self.view.controls.extend([
                Container(
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.symmetric(horizontal=5),
                    content=Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            self.selection_table, 
                            self.confirmation_message
                        ]
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
                        ft.Icon(ft.Icons.EDIT, color=ft.Colors.LIGHT_GREEN_700, size=20),
                        Text(
                            value=f'Edit Game #{self.seleted_match}?',
                            size=13,
                            color=ft.Colors.LIGHT_GREEN_900,
                        ),
                    ]
                ),
                Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(width=100, content="Cancel", on_click=self.disable_edit),
                        ft.Button(
                            width=100,
                            content="Edit",
                            on_click=self.confirmed_edit,
                            bgcolor=ft.Colors.LIGHT_GREEN_600,
                            color=ft.Colors.WHITE,
                        ),
                    ]
                ),
            ]
        )

        self.confirmation_message.visible = True
        self.confirmation_message.content = controls
        self.app_page.update()

    def disable_edit(self, e=None):
        self.confirmation_message.visible = False
        self.confirmation_message.content = None
        self.app_page.update()
        self.seleted_match = ''
        self.form_builder = ''

    def confirmed_edit(self, e=None):
        self.confirmation_message.visible = False
        self.confirmation_message.content = None
        
        self.form_builder = FormBuilder(
                        page=self.app_page, 
                        on_click_function= lambda e: self.edit_match(self.seleted_match),
                        match=self.all_matches[int(self.seleted_match)]
                    )
        
        self.view.controls = [
            UniversalAppBar(self.app_page),
            Row(
                controls=[Text(value="Edit Match", size=20)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Divider(),
            self.form_builder
        ]
        self.app_page.update()
        
    async def update_page_on_success(self):
        route = self.app_page.route
        self.seleted_match = ''
        self.form_builder = ''
        await self.app_page.push_route('')
        await self.app_page.push_route(route)
    
    def edit_match(self, match_number, e=None):
        assert isinstance(self.form_builder, FormBuilder)
        
        original_match = self.all_matches[match_number]
        
        data = {}
        for key, control in self.form_builder.form_fields.items(): 
            if isinstance(control, (UniversalTextInputField, UniversalFloatInputField,UniversalNumberInputField, UniversalDropdownInput)):
                data[key] = control.value
                
            elif isinstance(control, UniversalDateInput):
                data["date"] = control.selected_date
            
            
        
        result, returned_value = self.state.edit_match(match_number = match_number, edited_match = data)
        
        if result:
            asyncio.create_task(self.update_page_on_success())
        
        else:
            self.form_builder.error_container.visible = True
            self.form_builder.error_column.visible = True
            self.form_builder.error_container.bgcolor = ft.Colors.RED_100
            self.form_builder.error_column.controls = [Text("Errors:")]
            self.form_builder.error_column.controls.append(Text(f'1. {returned_value}'))
                
            self.app_page.update()        
    
        