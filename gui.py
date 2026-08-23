#Misc Imports 
from typing import Any
import asyncio
import datetime

#File imports
from backend.validation import validate_match_result,validate_player_discipline,validate_player_role,validate_player_stats,general_validation
from backend.input_validation_gui import general_input_check
from backend.database import load_all_matches,init_database, save_match
from backend.stats import show_summary

#Flet Imports
import flet as ft
from flet import Row, Column, Container, Text, VerticalDivider

infinite_int = 10**18

#Custom Unique Controls (Appbar, Navigation Drawer, Stat Containers) --------
@ft.control
class UniversalAppBar(ft.AppBar):
    def __init__(self, page: ft.Page) -> None:
        self.app_page = page
        
        self.menu_button = ft.IconButton(
                icon=ft.Icons.MENU, 
                hover_color=ft.Colors.GREY_300,
                on_click= self.show_drawer
            )
        
        super().__init__(
            leading= self.menu_button,
            title = ft.Text(value="Soccer Statistics Tracker",size=19),
            bgcolor = ft.Colors.GREY_200
        )
        
    async def show_drawer(self, e):
        await self.app_page.show_drawer()

@ft.control
class NavigationMenu(ft.NavigationDrawer):
    def __init__(self, page) -> None:
        self.app_page = page
                
        self.routes = {
            0 : '/home',
            1 : '/add'
        }
        
        super().__init__(
            tile_padding=3,
            on_change = self.handle_change,
            controls=[
                    ft.Container(
                        content=ft.Text(
                            value="Navigate", 
                            size=17, 
                            align=ft.Alignment.CENTER_LEFT, 
                            font_family='Chiron GoRound TC',
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                        ), 
                        padding=ft.Padding.only(left=28, top=20, bottom=12),
                    ),
                    ft.Divider(),
                    ft.NavigationDrawerDestination(label='Home', icon=ft.Icons.HOME, selected_icon=ft.Icons.HOME_FILLED),
                    ft.NavigationDrawerDestination(label='Add Match', icon=ft.Icons.CREATE_OUTLINED, selected_icon=ft.Icons.CREATE),
                    ft.NavigationDrawerDestination(label='All Matches', icon=ft.Icons.LIST_OUTLINED, selected_icon=ft.Icons.LIST),
                    ft.NavigationDrawerDestination(label='Specific Match', icon=ft.Icons.SEARCH_OUTLINED, selected_icon=ft.Icons.SEARCH),
                    ft.NavigationDrawerDestination(label='Season Summary', icon=ft.Icons.STACKED_BAR_CHART_OUTLINED, selected_icon=ft.Icons.STACKED_BAR_CHART),
                    ft.NavigationDrawerDestination(label='Edit Match', icon=ft.Icons.EDIT_OUTLINED, selected_icon=ft.Icons.EDIT),
                    ft.NavigationDrawerDestination(label='Delete Match', icon=ft.Icons.DELETE_OUTLINED, selected_icon=ft.Icons.DELETE),
                ]
        )
    
    async def handle_change(self,e: ft.Event[ft.NavigationDrawer]):
        route = self.routes.get(e.control.selected_index)
        
        if route:
            print(f'seleted: {route}')
            await self.app_page.push_route(route=route)

        else:
            print("ok so were firing 'bullshit' route ")
            await self.app_page.push_route(route='bullshit')
            
        
        await self.page.close_drawer()

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



class Add_Match():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        self.error_column = Column(
            disabled=True,
            controls=[],
        )
        
        self.error_container = Container(
            disabled=True,
            width = 275,
            content=self.error_column,
            border_radius=ft.BorderRadius.all(5),
            padding=ft.Padding.all(15)
        )
        
        self.positions = [
            "Goalkeeper",
            "Center Back",
            "Left Back",
            "Right Back",
            "Fullback",
            "Left Wing Back",
            "Right Wing Back",
            "Wing Back",
            "Defensive Midfielder",
            "Central Midfielder",
            "Attacking Midfielder",
            "Left Midfielder",
            "Right Midfielder",
            "Left Wing",
            "Right Wing",
            "Winger",
            "Center Forward",
            "Striker",
            "Second Striker",
            "Sweeper",
            "Bench",
            "Multiple Positions",
        ]
                
        
        self.input_controls = {
            #Ts is very unoptiomized i think 
            #i hope that i can use like an if statement and cancel out all the ft.dividers and ft.text stuff
            #otherwise im cooked 😭
            #Im sorry to future me who has to add shi to this, atp js make a different @ft.control class for it 
            
            #Match Data -----------
            "text1": ft.Text(value="Match Data",size=14),
            "opponent_name": UniversalTextInputField(page=self.app_page,label="Opponent Name"),
            "date": UniversalDateInput(page=self.app_page),
            "competition": UniversalTextInputField(page=self.app_page,label="Competition"),
            "divider1": ft.Divider(),
            
            #Result ---------------
            "text2": ft.Text(value="Result",size=14),
            "result": UniversalDropdownInput(page = self.app_page, label="Result", option_values=["Win","Loss","Draw"]),
            "your_goals": UniversalNumberInputField(page=self.app_page,label="Your Goals",lower_bound=0,upper_bound=infinite_int),
            "opponents_goals": UniversalNumberInputField(page=self.app_page,label="Opponents Goals",lower_bound=0,upper_bound=infinite_int),
            "divider2": ft.Divider(),
            
            #Player Role/Minutes/Position -----------
            "text3": ft.Text(value="Role/Minutes/Position",size=14),
            "role": UniversalDropdownInput(page = self.app_page, label="Role", option_values=["Starter","Substitute"]),
            #TODO: If you ever wanna add sum, add a checkbox here with the label "Went to Extra Time?"
            "minutes_played": UniversalNumberInputField(page=self.app_page,label="Minutes",lower_bound=0,upper_bound=120),
            # TODO: swap position field to UniversalAutoCompleteInput once label + focus-border are sorted
            "position":  UniversalDropdownInput(page=self.app_page, label="Position", option_values=self.positions),
            "divider3": ft.Divider(),
            
            #Player Match Stats ----------
            "text4": ft.Text(value="Player Match Stats",size=14),
            "goals": UniversalNumberInputField(page=self.app_page,label="Goals",lower_bound=0,upper_bound=infinite_int),
            "assists": UniversalNumberInputField(page=self.app_page,label="Assists",lower_bound=0,upper_bound=infinite_int),
            "divider4": ft.Divider(),
            
            #Player Discipline
            "text5": ft.Text(value="Player Discipline",size=14),
            "yellow_cards": UniversalNumberInputField(page=self.app_page,label="Yellow Cards",lower_bound=0,upper_bound=2),
            "red_cards": UniversalNumberInputField(page=self.app_page,label="Red Cards",lower_bound=0,upper_bound=1),
            "divider5": ft.Divider(),
            
            #Confidence
            "text6": ft.Text(value="Confidence (0-10)",size=14),
            "confidence": UniversalFloatInputField(page=self.app_page,label="Confidence",lower_bound=0,upper_bound=10),
            "divider6": ft.Divider(),
            
            #Notes
            "text7": ft.Text(value="Notes",size=14),
            "notes": UniversalTextInputField(page=self.app_page,label="Notes"),
            "divider7": ft.Divider()
        }
        
        self.view = ft.View(
            drawer=self.nav_menu,
            padding= ft.Padding(0,0,0,20),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                UniversalAppBar(self.app_page),
                *self.input_controls.values(),
                self.error_container,
                ft.Button(
                    width=100,
                    height = 30,
                    content="Submit",
                    on_click=self.save_data,
                    bgcolor=ft.Colors.GREEN_200,
                    elevation=3,
                )
            ]
        )
        
    def save_data(self,e):
        data = {}
        for control in self.input_controls.values():
            if isinstance(control, (UniversalTextInputField, UniversalFloatInputField,UniversalNumberInputField, UniversalDropdownInput)):
                data[str(control.label)] = control.value
                
            elif isinstance(control, UniversalDateInput):
                data["Date"] = control.selected_date
        
        result, returned_value = self.state.save_data(data)
        
        if result:
            self.error_container.disabled = False
            self.error_column.disabled = False
            self.error_container.bgcolor = ft.Colors.GREEN_100
            self.error_column.controls = [Text("Success! Game added to database.")]
            
            for control in self.input_controls.values():
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
            self.error_container.disabled = False
            self.error_column.disabled = False
            self.error_container.bgcolor = ft.Colors.RED_100
            self.error_column.controls = [Text("Errors:")]
            for index,value in enumerate(unique_returned_values,1):
                self.error_column.controls.append(Text(f'{index}. {value}'))
                
            self.app_page.update()
                  

class HomePage():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        data_dict = [
            [self.state.all_matches_summary['wins'],'Wins'],
            [self.state.all_matches_summary['draws'],'Draws'],
            [self.state.all_matches_summary['losses'],'Losses']
        ]
        
        self.view = ft.View(
            drawer=self.nav_menu,
            padding= ft.Padding.all(0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                UniversalAppBar(self.app_page),
                StatRow(self.app_page,data_dict)
            ]
        )

class Error404_NotFound_Page():
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
                Text(value="How the fuck did your ass get here lmao")
            ]
        )

#Main soure of app data
#basically links the database/backend to the frontend/gui
class AppState:
    #Anything can update this, since it passes into every view
    def __init__(self):
        self.all_matches_summary = {}

    def refresh(self):
        all_matches = load_all_matches()
        data = show_summary(all_matches=all_matches)
        
        self.all_matches_summary = data
    
    def save_data(self,data_dict):
        #Validate Data
        errors = {}
        match = {}
        
        for field_name, value in data_dict.items():
            key = field_name.lower().replace(" ","_")
            result, value = general_input_check(key,value)
            if not result:
                errors[key] = value
            else:
                match[key] = value
        
        #Return if specific values are flawed
        if len(errors) > 0:
            print(errors)
            return False, errors
        
        validation_result, returned_value = general_validation(match)
        
        #Send Data to Database
        if not validation_result:
            errors["match"] = value
            print(errors)
            return False, errors
            
        save_match(match)
        return True, None
            
    
class Router():
    @staticmethod
    def get_views(route, general_controls):
        match route:
            case '/home':
                return HomePage(*general_controls).view
            case '/add':
                return Add_Match(*general_controls).view    
            case _:
                return Error404_NotFound_Page(*general_controls).view

class App():
    def __init__(self,page,state) -> None:
        self.page :ft.Page = page
        self.nav_menu = NavigationMenu(self.page)
        self.state = state
        
        self.general_controls = [self.page, self.state, self.nav_menu]
        
        self.page.on_route_change = self.route_change
    
    def route_change(self, e = None):
        self.page.views.clear()
        self.state.refresh()
        print('yea ok so we got this route:',self.page.route)
        new_view = Router.get_views(self.page.route, self.general_controls)
        self.page.views.append(new_view)
        self.page.update()


#Initalize the app and hand it off the App() class
def main(page: ft.Page) -> None:
    init_database()
    page.route = '/home'
    page.title = "Soccer Statistics Tracker"
    page.window.width = 390
    page.window.height = 844
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    
    state = AppState()
    app = App(page,state)
    
    app.route_change()
     
if __name__ == "__main__":
    ft.run(main=main, assets_dir='assets')