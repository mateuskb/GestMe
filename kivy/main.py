import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

sys.path.append('./')
from inc.Classes.Requests import Requests
from inc.consts.consts import Consts

# Redirects
from pages.gestme.gestme import GestMeWindow
from pages.login.login import LogInWindow
from pages.signup.signup import SignUpWindow


class MainWindow(BoxLayout):
    
    gestme_widget = GestMeWindow()
    login_widget = LogInWindow()
    signup_widget = SignUpWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.gestme_screen.add_widget(self.gestme_widget)
        self.ids.login_screen.add_widget(self.login_widget)
        self.ids.signup_screen.add_widget(self.signup_widget)
        
    def consts(self):
        return Consts()


class MainApp(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MainApp().run()