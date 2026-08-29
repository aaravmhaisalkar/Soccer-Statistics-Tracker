#Misc Imports 
import inspect

#File imports
from backend.rules import gui_positions, infinite_int
from frontend.controls.universal_controls import UniversalDateInput,UniversalDropdownInput,UniversalFloatInputField,UniversalNumberInputField,UniversalTextInputField

#Flet Imports
import flet as ft
from flet_datatable2 import DataTable2, DataColumn2, DataColumnSize, DataRow2
from flet import Row, Column, Container, Text, VerticalDivider


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
            1 : '/add',
            2 : '/all_matches',
            3 : '/specific_match',
            4 : '/summary',
            5 : '/edit',
            6 : '/delete'
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
            await self.app_page.push_route(route='_')
            
        
        await self.page.close_drawer()

@ft.control
class FormBuilder(Container):
    def __init__(self, page: ft.Page, on_click_function, match = None) -> None:
        self.app_page = page
        self.on_click_function = on_click_function
        self.match = match
        
        self.error_column = Column(
                    visible=False,
                    controls=[],
                )
                
        self.error_container = Container(
            visible=False,
            width = 275,
            content=self.error_column,
            border_radius=ft.BorderRadius.all(5),
            padding=ft.Padding.all(15)
        )
                
        
        self.form_fields = {
            #Match Data -----------
            "opponent_name": UniversalTextInputField(page=self.app_page,label="Opponent Name"),
            "date": UniversalDateInput(page=self.app_page),
            "competition": UniversalTextInputField(page=self.app_page,label="Competition"),
            
            #Result ---------------
            "result": UniversalDropdownInput(page = self.app_page, label="Result", option_values=["Win","Loss","Draw"]),
            "your_goals": UniversalNumberInputField(page=self.app_page,label="Your Goals",lower_bound=0,upper_bound=infinite_int),
            "opponents_goals": UniversalNumberInputField(page=self.app_page,label="Opponents Goals",lower_bound=0,upper_bound=infinite_int),
            
            #Player Role/Minutes/Position -----------
            "role": UniversalDropdownInput(page = self.app_page, label="Role", option_values=["Starter","Substitute"]),
            #TODO: If you ever wanna add sum, add a checkbox here with the label "Went to Extra Time?"
            "minutes": UniversalNumberInputField(page=self.app_page,label="Minutes",lower_bound=0,upper_bound=120),
            # TODO: swap position field to UniversalAutoCompleteInput once label + focus-border are sorted
            "position":  UniversalDropdownInput(page=self.app_page, label="Position", option_values=gui_positions),
            
            #Player Match Stats ----------
            "goals": UniversalNumberInputField(page=self.app_page,label="Goals",lower_bound=0,upper_bound=infinite_int),
            "assists": UniversalNumberInputField(page=self.app_page,label="Assists",lower_bound=0,upper_bound=infinite_int),
            
            #Player Discipline
            "yellow_cards": UniversalNumberInputField(page=self.app_page,label="Yellow Cards",lower_bound=0,upper_bound=2),
            "red_cards": UniversalNumberInputField(page=self.app_page,label="Red Cards",lower_bound=0,upper_bound=1),
            
            #Confidence
            "confidence": UniversalFloatInputField(page=self.app_page,label="Confidence",lower_bound=0,upper_bound=10),
            
            #Notes
            "notes": UniversalTextInputField(page=self.app_page,label="Notes"),
        }

    
        self.form_schema = {
            "Match Data": ["opponent_name", "date", "competition"],
            "Result": ["result", "your_goals", "opponents_goals"],
            "Role/Minutes/Position": ["role", "minutes", "position"],
            "Player Match Stats": ["goals", "assists"],
            "Player Discipline": ["yellow_cards", "red_cards"],
            "Confidence (0-10)": ["confidence"],
            "Notes": ["notes"],
        }
        
        self.form = []
        
        
        for heading, fields in self.form_schema.items():
            self.form.append(ft.Text(value=heading,size=14))
            
            for field in fields:
                if self.match is not None:
                    if isinstance(self.form_fields[field], UniversalDateInput):
                        self.form_fields[field].date_selected_text.value = self.match[field]
                        self.form_fields[field].date_picker.value = self.match[field]
                        self.form_fields[field].selected_date = self.match[field]
                    elif isinstance(self.form_fields[field], UniversalDropdownInput):
                         self.form_fields[field].value = self.match[field]
                    else:
                        self.form_fields[field].value = self.match[field]
                
                self.form.append(self.form_fields[field])
                

            
            self.form.append(ft.Divider())
        
        self.form.extend([
            self.error_container,
            ft.Button(
                width=100,
                height = 30,
                content="Submit",
                on_click=self.on_click_function,
                bgcolor=ft.Colors.GREEN_200,
                elevation=3,
            )
        ])
        
        super().__init__(
            content=Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=self.form
            )
        )

#For All Matches - Less info just basics (name, date, goals/assists, ect...).
#Hooked up to any function given, and on click can go to it / do the action.
@ft.control
class MatchDisplayTable_SMALL(Container):
    def __init__(self, page: ft.Page, state, data, nav_menu, on_tap_function) -> None:
        self.app_page = page
        self.data = data
        self.state = state
        self.nav_menu = nav_menu
        self.on_tap_function = on_tap_function
        
        self.row_list = []
        
        def handle_tap():
            if inspect.iscoroutinefunction(self.on_tap_function):
                return lambda e, num = id: self.app_page.run_task(self.on_tap_function ,e,num)
            else:
                return lambda e, num = id: self.on_tap_function(e,num)
                
        
        for id, match in self.data.items():
            self.row_list.append(
                DataRow2(
                    cells=[
                        ft.DataCell(content=ft.Text(str(id))),
                        ft.DataCell(content=ft.Text(f'{match['opponent_name']}')),
                        ft.DataCell(content=ft.Text(f'{match['date']}')),
                        ft.DataCell(content=ft.Text(f'{match['result']}')),
                        ft.DataCell(content=ft.Text(f'{match['your_goals']}-{match['opponents_goals']}')),
                        ft.DataCell(content=ft.Text(str(match['goals']))),
                        ft.DataCell(content=ft.Text(str(match['assists'])))
                    ],
                    on_tap= handle_tap()
                )
            )
        
        super().__init__(
            border=ft.Border.all(1, ft.Colors.BLACK),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(5),
            content=Row(
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    DataTable2(
                        width=1000,
                        columns=[
                            DataColumn2(size=DataColumnSize.S, label=ft.Text("#"), tooltip="Number", numeric=True),
                            DataColumn2(size=DataColumnSize.L, label=ft.Text("Opponent"), tooltip="Opponent"),
                            DataColumn2(size=DataColumnSize.L, label=ft.Text("Date"), tooltip="Date"),
                            DataColumn2(size=DataColumnSize.M, label=ft.Text("Result"), tooltip="Result"),
                            DataColumn2(size=DataColumnSize.M, label=ft.Text("Score"), tooltip="Your Goals - Opponent Goals"),
                            DataColumn2(size=DataColumnSize.M, label=ft.Text("Goals"), tooltip="Goals Scored", numeric=True),
                            DataColumn2(size=DataColumnSize.M, label=ft.Text("Assists"), tooltip="Assists", numeric=True),
                        ],
                        rows=self.row_list
                    )
                ]
            )
        )
        
#Full rundown on a match - All stats from the database.
@ft.control
class MatchDisplayTable_FULL(Container):
    def __init__(self, page: ft.Page, data, number) -> None:
        self.app_page = page
        self.data = data
        self.number = number
        
        
        def detail_row(label, value):
                    return Row(
                        controls=[
                            Text(value=label, size=13, color=ft.Colors.GREY_600, width=110),
                            Text(value=str(value) if value != "" else "-", size=13, weight=ft.FontWeight.W_500),
                        ]
                    )
                
        def section_header(title):
            return Text(value=title, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        
        super().__init__(
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(16),
            bgcolor=ft.Colors.WHITE,
            content=Column(
                spacing=10,
                controls=[
                    Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text(value=f"Match #{self.number}", size=16, weight=ft.FontWeight.BOLD),
                            Text(value=self.data["date"], size=13, color=ft.Colors.GREY_600),
                        ]
                    ),
                    ft.Divider(),
                    
                    section_header("Match Data"),
                    detail_row("Opponent", self.data["opponent_name"]),
                    detail_row("Competition", self.data["competition"]),
                    detail_row("Result", self.data["result"]),
                    detail_row("Score", f'{self.data["your_goals"]}-{self.data["opponents_goals"]}'),
                    ft.Divider(),
                    
                    section_header("Role"),
                    detail_row("Position", self.data["position"]),
                    detail_row("Role", self.data["role"]),
                    detail_row("Minutes", self.data["minutes"]),
                    ft.Divider(),
                    
                    section_header("Performance"),
                    detail_row("Goals", self.data["goals"]),
                    detail_row("Assists", self.data["assists"]),
                    detail_row("Confidence", f'{self.data["confidence"]}/10'),
                    ft.Divider(),
                    
                    section_header("Discipline"),
                    detail_row("Yellow Cards", self.data["yellow_cards"]),
                    detail_row("Red Cards", self.data["red_cards"]),
                    ft.Divider(),
                    
                    section_header("Notes"),
                    Text(value=self.data["notes"] if self.data["notes"] else "No notes recorded.", size=13),
                ]
            )
        )

#Replica of MatchDisplayTable_FULL, but specifically for FULL season stat display
@ft.control
class SeasonStatsDisplayTable(Container):
    def __init__(self, page: ft.Page, data) -> None:
        self.app_page = page
        self.data = data
        
        def detail_row(label, value):
                    return Row(
                        controls=[
                            Text(value=label, size=13, color=ft.Colors.GREY_600, width=110),
                            Text(value=str(value) if value != "" else "-", size=13, weight=ft.FontWeight.W_500),
                        ]
                    )
                
        def section_header(title):
            return Text(value=title, size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800)

        
        super().__init__(
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(16),
            bgcolor=ft.Colors.WHITE,
            content=Column(
                spacing=10,
                controls=[
                    Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text(value=f"Season Stats", size=16, weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Divider(),
                    
                    section_header("Season Overview"),
                    detail_row("Total Matches", self.data["total_matches"]),
                    detail_row("Wins", self.data["wins"]),
                    detail_row("Draws", self.data["draws"]),
                    detail_row("Losses", self.data["losses"]),
                    detail_row("Win Percentage", f'{self.data["win_percentage"]:.1f}%'),
                    ft.Divider(),

                    section_header("Performance"),
                    detail_row("Goals", self.data["total_goals"]),
                    detail_row("Assists", self.data["total_assists"]),
                    detail_row("Minutes Played", self.data["total_min_played"]),
                    detail_row("Average Confidence", f'{self.data["average_confidence"]:.1f}/10'),
                    ft.Divider(),

                    section_header("Team Performance"),
                    detail_row("Goals For", self.data["goals_for"]),
                    detail_row("Goals Against", self.data["goals_against"]),
                    detail_row("Goal Differential", f'{self.data["goal_differential"]:+d}'),
                    ft.Divider(),

                    section_header("Discipline"),
                    detail_row("Yellow Cards", self.data["total_yellow_cards"]),
                    detail_row("Red Cards", self.data["total_red_cards"]),
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
