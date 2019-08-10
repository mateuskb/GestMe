import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

sys.path.append('../')
from request.Classes.Requests import Requests
from consts.consts import Consts

# Redirects
from pages.login.login import LogInApp, LogInWindow
from pages.signup.signup import SignUpApp, SignUpWindow

class GestMeWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def consts(self):
        return Consts()

    def redirect_login(self):
        LogInApp().run()
    
    def redirect_signup(self):
        SignUpApp().run()

# sm = ScreenManager()

class GestMeApp(App):

    def build(self):
        return GestMeWindow()

if __name__ == '__main__':
    GestMeApp().run()