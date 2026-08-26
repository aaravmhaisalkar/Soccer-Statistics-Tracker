#Misc Imports 
from typing import Any
import asyncio
import inspect
import datetime

#File imports
from backend.validation import general_validation
from backend.input_validation_gui import general_input_check
from backend.display import display_all_matches
from backend.database import load_all_matches,init_database, save_match, delete_match
from backend.stats import show_summary
from backend.rules import gui_positions
#Control Imports
from universal_controls import UniversalDateInput,UniversalDropdownInput,UniversalFloatInputField,UniversalNumberInputField,UniversalTextInputField

#Flet Imports
import flet as ft
from flet_datatable2 import DataTable2, DataColumn2, DataColumnSize, DataRow2
from flet import Row, Column, Container, Text, VerticalDivider

infinite_int = 10**18

#RUN on iOS = flet run gui.py --ios --name SoccerStatisticsTracker


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



#PAGES ----------------------------------------------

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

#Page for displaying all matches. Simpler data compared to specific match page.
class All_Matches_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
        self.view = ft.View(
                    drawer=self.nav_menu,
                    padding= ft.Padding.all(0),
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        UniversalAppBar(self.app_page),
                        Container(
                            padding=ft.Padding.symmetric(horizontal=5),
                            content=Column(
                                controls = [
                                    Row(
                                        controls=[
                                            Text(value="All Matches", size=20)
                                        ], 
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    ft.Divider(),
                                ]
                            )
                        ),
                    ]
                )  
        
        
        self.all_matches = self.state.all_matches
        
        self.all_matches_datatable = MatchDisplayTable_SMALL(
            page=self.app_page,
            state=self.state,
            data=self.all_matches,
            nav_menu=self.nav_menu, 
            on_tap_function= self.navigate_to_full_data
        )
        
        errors = self.state.build_status_message()
        
        if errors != None:
            self.view.controls.append(errors)
            
        else:
            self.view.controls.extend([
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color=ft.Colors.GREY_600),
                        Text("For full match details, click on the game data row.", size=11, color=ft.Colors.GREY_600),
                    ]
                ),
                ft.Divider(),
                Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[self.all_matches_datatable],
                ),
                Row(
                    controls=[
                        ft.Icon(ft.Icons.SWIPE, size=17, color=ft.Colors.GREY_500),
                        ft.Text("Scroll for more", size=14, color=ft.Colors.GREY_500),
                    ], 
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ])
        
        
        
        
        
    async def navigate_to_full_data(self,e, num):
        self.nav_menu.selected_index = 3
        self.state.all_match_selected_match_id = int(num)
        await self.app_page.push_route('/specific_match')

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

#Add Match Page
class Add_Match_Page():
    def __init__(self, page, state, nav_menu) -> None:
        self.app_page = page
        self.state = state
        self.nav_menu = nav_menu
        
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
            "position":  UniversalDropdownInput(page=self.app_page, label="Position", option_values=gui_positions),
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
                Row(
                    controls=[Text(value="Add Match", size=20)],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Divider(),
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
            self.error_container.visible = True
            self.error_column.visible = True
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
            self.error_container.visible = True
            self.error_column.visible = True
            self.error_container.bgcolor = ft.Colors.RED_100
            self.error_column.controls = [Text("Errors:")]
            for index,value in enumerate(unique_returned_values,1):
                self.error_column.controls.append(Text(f'{index}. {value}'))
                
            self.app_page.update()        

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
        
        

#Error page, kinda obvious
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
                Text(value="Error 404: Page Not Found")
            ]
        )



#APP STATE/ APP / ROUTER ----------------------------


#Main soure of app data
#basically links the database/backend to the frontend/gui
class AppState:
    #Anything can update this, since it passes into every view
    def __init__(self):
        #Good = good data, bad = error in data, empty = no data
        self.data_status = "" 
        self.all_match_selected_match_id = ''
        self.all_matches = {}
        self.all_matches_summary = {}

    def refresh(self):
        all_matches_check, all_matches = load_all_matches()
        
        if not all_matches_check:
            self.data_status = "bad"
            all_matches = {}
            return
    
        
        #We do this 'usable_all_matches' thing bc sqlite3 returns sqlite.Row objects not "good" data
        useable_data_check, usable_all_matches_data = display_all_matches(all_matches=all_matches)
        summery_check, summery_data = show_summary(all_matches=all_matches)
        
        if summery_check and useable_data_check:
            self.data_status = "good"
            self.all_matches_summary = summery_data
            self.all_matches = usable_all_matches_data
            return
        
        else:
            self.data_status = "empty"
            return
    
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
            errors["match"] = returned_value
            print(errors)
            return False, errors
            
        result, error = save_match(match)
        
        if not result:
            errors["database"] = error
            return False, errors
        
        return True, None
    
    def delete_match(self, match_number):
        result, error = delete_match(match_number)
        if result:
            return True, None
        else:
            return False, error
        
    def build_status_message(self):
        match self.data_status:
            case "bad":
                return Text("Something went wrong loading data.", color=ft.Colors.RED)
            case "empty":
                return Text("No matches yet — add your first one!")
            case _:
                return None
     
#Different pages routing connector
class Router():
    @staticmethod
    def get_views(route, general_controls):
        match route:
            case '/home':
                return HomePage(*general_controls).view
            case '/add':
                return Add_Match_Page(*general_controls).view  
            case '/all_matches':
                return  All_Matches_Page(*general_controls).view
            case '/specific_match':
                return  Specific_Match_Page(*general_controls).view
            case '/summary':
                return  Season_Summary_Page(*general_controls).view
            
            
            case '/delete':
                return  Delete_Match_Page(*general_controls).view
            case _:
                return Error404_NotFound_Page(*general_controls).view

#Main app class, honestly not that important feature-wise
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



#RUN PROGRAM / INIT --------------------


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