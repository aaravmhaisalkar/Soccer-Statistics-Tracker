#Control Imports
from frontend.controls.universal_controls import UniversalDateInput,UniversalDropdownInput,UniversalFloatInputField,UniversalNumberInputField,UniversalTextInputField
from frontend.controls.unique_controls import UniversalAppBar, FormBuilder

#Flet Imports
import flet as ft
from flet import Row, Text

#Add Match Page
class Add_Match_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        
        self.form_builder = FormBuilder(page=self.app_page, on_click_function=lambda e: self.save_data())
        
        self.view = ft.View(
            drawer=self.nav_menu,
            padding= ft.Padding(0,0,0,20),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                Row(
                    controls=[Text(value="Add Match", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
                self.form_builder,
            ]
        )
        
    def save_data(self,e=None):
        data = {}
        for key, control in self.form_builder.form_fields.items():
            if isinstance(control, (UniversalTextInputField, UniversalFloatInputField,UniversalNumberInputField, UniversalDropdownInput)):
                data[key] = control.value
                
            elif isinstance(control, UniversalDateInput):
                data["date"] = control.selected_date
                
        result, returned_value = self.state.save_data(data)
        
        if result:
            self.form_builder.error_container.visible = True
            self.form_builder.error_column.visible = True
            self.form_builder.error_container.bgcolor = ft.Colors.GREEN_100
            self.form_builder.error_column.controls = [Text("Success! Game added to database.")]
            
            for _, control in self.form_builder.form_fields.items():
                if isinstance(control, (UniversalTextInputField, UniversalFloatInputField,UniversalNumberInputField)):
                    control.value = ""
                                
                elif isinstance(control, UniversalDropdownInput):
                    control.value = None
                                
                elif isinstance(control, UniversalDateInput):
                    control.selected_date = ""
                    control.date_selected_text.value = ""

            
            self.app_page.update()
        
        else:
            unique_returned_values = set(returned_value.values())
            self.form_builder.error_container.visible = True
            self.form_builder.error_column.visible = True
            self.form_builder.error_container.bgcolor = ft.Colors.RED_100
            self.form_builder.error_column.controls = [Text("Errors:")]
            for index,value in enumerate(unique_returned_values,1):
                self.form_builder.error_column.controls.append(Text(f'{index}. {value}'))
                
            self.app_page.update()        
