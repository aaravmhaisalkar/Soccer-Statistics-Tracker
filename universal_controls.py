#Misc Imports 
import datetime
#Flet Imports
import flet as ft

#Universal Controls (Text, Number, Dropdown, Float) -------------
@ft.control
class UniversalTextInputField(ft.TextField):
    def __init__(self, page: ft.Page, label) -> None:
        self.app_page = page  
        
        super().__init__(
            label=label,
        )

@ft.control
class UniversalNumberInputField(ft.TextField):
    def __init__(self, page: ft.Page, label, lower_bound, upper_bound) -> None:
        self.app_page = page  
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        
        super().__init__(
            label=label,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter= ft.NumbersOnlyInputFilter(),
            on_blur = self.limit_inputs
        )
        
    def limit_inputs(self, e):
        if e.control.value != "":
            value = int(e.control.value)
            
            if self.lower_bound <= value <= self.upper_bound:
                pass
            else:
                e.control.value = ""
              
@ft.control
class UniversalFloatInputField(ft.TextField):
    def __init__(self, page: ft.Page, label, lower_bound, upper_bound) -> None:
        self.app_page = page  
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super().__init__(
            label=label,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter= ft.InputFilter(
                allow=True,
                regex_string=r"^\d*\.?\d*$",
                replacement_string=""
            ),
            on_blur = self.limit_inputs
        )
        
    def limit_inputs(self, e):
        if e.control.value != "":
            value = float(e.control.value)
            if self.lower_bound <= value <= self.upper_bound:
                pass
            else:
                e.control.value = ""
      
@ft.control  
class UniversalDropdownInput(ft.Dropdown):
    def __init__(self, page: ft.Page, label,option_values) -> None:
        self.app_page = page  
        self.option_list = []
        self.option_values = option_values
        
        for option in self.option_values:
            self.option_list.append(ft.DropdownOption(key=option.lower(), text=option.title()))
            
        
        super().__init__(
            label=label,
            options= self.option_list
        )

@ft.control  
class UniversalDateInput(ft.Container):
    def __init__(self, page: ft.Page) -> None:
        self.app_page = page  
        
        self.today = datetime.datetime.today()
        self.selected_date = datetime.datetime.today().strftime('%m/%d/%Y')
        self.date_selected_text = ft.Text(value="", size=15)

        
        self.date_picker = ft.DatePicker(
            last_date=self.today,
            current_date=self.today,
            on_change=self.date_picked,
        )

        
        super().__init__(
            width=300,
            height=50,
            padding=ft.Padding.all(8),
            border_radius=ft.BorderRadius.all(4),
            border=ft.Border.all(1, ft.Colors.BLACK),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.date_selected_text,
                    ft.Button(
                        width=140,
                        icon=ft.Icons.CALENDAR_MONTH, 
                        content="Pick Date", 
                        on_click=lambda _: self.app_page.show_dialog(self.date_picker)
                    )
                ]
            )
        )
    
    def date_picked(self, e):
        self.selected_date = e.control.value.strftime('%m/%d/%Y')
        self.date_selected_text.value = f'{self.selected_date}'

