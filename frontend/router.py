#Import Pages
from frontend.pages.homepage import HomePage
from frontend.pages.add_match import Add_Match_Page
from frontend.pages.all_matches import All_Matches_Page
from frontend.pages.specific_match import Specific_Match_Page
from frontend.pages.season_summary import Season_Summary_Page
from frontend.pages.edit_match import Edit_Match_Page
from frontend.pages.delete_match import Delete_Match_Page
from frontend.pages.error_404 import Error404_NotFound_Page
from frontend.pages.auth_page import Auth_Page
from frontend.pages.loading_page import Loading_Page
from frontend.pages.account_page import Account_Page

#Different pages routing connector
class Router():
    @staticmethod
    def get_views(route, general_controls):
        match route:
            case '/auth':
                return Auth_Page(*general_controls).view
            case '/home':
                return HomePage(*general_controls).view
            case '/add':
                return Add_Match_Page(*general_controls).view  
            case '/all_matches':
                return  All_Matches_Page(*general_controls).view
            case '/specific_match':
                return  Specific_Match_Page(*general_controls).view
            case '/summary':
                return Season_Summary_Page(*general_controls).view
            case '/edit':
                return Edit_Match_Page(*general_controls).view
            case '/delete':
                return  Delete_Match_Page(*general_controls).view
            case '/loading':
                return Loading_Page(*general_controls).view
            case '/account':
                return Account_Page(*general_controls).view
            case _:
                return Error404_NotFound_Page(*general_controls).view
