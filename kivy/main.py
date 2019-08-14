import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

sys.path.append('./')
from inc.classes.Requests import Requests
from inc.consts.consts import Consts

# Redirects
from pages.gestme.gestme import GestMeWindow
from pages.login.login import LogInWindow
from pages.signup.signup import SignUpWindow
from pages.signup.signupok import SignupokWindow


class MainWindow(BoxLayout):
    
    gestme_widget = GestMeWindow()
    login_widget = LogInWindow()
    signup_widget = SignUpWindow()
    signupok_widget = SignupokWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.gestme_screen.add_widget(self.gestme_widget)
        self.ids.login_screen.add_widget(self.login_widget)
        self.ids.signup_screen.add_widget(self.signup_widget)
        self.ids.signupok_screen.add_widget(self.signupok_widget)
        
    def consts(self):
        return Consts()

    def restart(self):
        self.root.clear_widgets()

class MainApp(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MainApp().run()