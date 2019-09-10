import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

BASE_PATH = os.path.abspath(__file__+ './')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.consts.consts import Consts

# Redirects
from pages.gestme.gestme import GestMeWindow
from pages.login.login import LogInWindow
from pages.signup.signup import SignUpWindow
from pages.signup.signupok import SignupokWindow
from pages.app.home.home import HomeWindow
from pages.app.app import AppWindow


class MainWindow(BoxLayout):
    
    gestme_widget = GestMeWindow()
    login_widget = LogInWindow()
    signup_widget = SignUpWindow()
    signupok_widget = SignupokWindow()
    app_app_widget = AppWindow()
    app_home_widget = HomeWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.gestme_screen.add_widget(self.gestme_widget)
        self.ids.login_screen.add_widget(self.login_widget)
        self.ids.signup_screen.add_widget(self.signup_widget)
        self.ids.signupok_screen.add_widget(self.signupok_widget)
        self.ids.app_app_screen.add_widget(self.app_app_widget)
        self.ids.app_home_screen.add_widget(self.app_home_widget)
        
    def consts(self):
        return Consts()

    def restart(self):
        self.root.clear_widgets()

class MainApp(App):

    def build(self):
        return MainWindow()
    
    def on_request_close(self, *args):
        self.textpopup(title='Exit', text='Are you sure?')
        return True

if __name__ == '__main__':
    MainApp().run()