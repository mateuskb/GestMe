import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition 

BASE_PATH = os.path.abspath(__file__+ './')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.consts.consts import Consts

# Redirects
from pages.gestme.gestme import GestMeWindow
from pages.login.login import LogInWindow
from pages.signup.signup import SignUpWindow
from pages.signup.signupok import SignupokWindow
from pages.app.app import AppWindow
from pages.app.home.home import HomeWindow


# class MainWindow(BoxLayout):
    
#     gestme_widget = GestMeWindow()
#     login_widget = LogInWindow()
#     signup_widget = SignUpWindow()
#     signupok_widget = SignupokWindow()

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.ids.gestme_screen.add_widget(self.gestme_widget)
#         self.ids.login_screen.add_widget(self.login_widget)
#         self.ids.signup_screen.add_widget(self.signup_widget)
#         self.ids.signupok_screen.add_widget(self.signupok_widget)
        
#     def consts(self):
#         return Consts()

#     def restart(self):
#         self.root.clear_widgets()
    
#     def load_app(self):
#         app_app_widget = AppWindow()
#         app_home_widget = HomeWindow()
#         self.ids.app_app_screen.add_widget(self.app_app_widget)
#         self.ids.app_home_screen.add_widget(self.app_home_widget)

sm = ScreenManager(transition=NoTransition())
sm.add_widget(GestMeWindow(name='gestme_screen'))
sm.add_widget(LogInWindow(name='login_screen'))
sm.add_widget(SignUpWindow(name='signup_screen'))
sm.add_widget(SignupokWindow(name='signupok_screen'))
# sm.add_widget(HomeWindow(name='app_home_screen'))

        
class MainApp(App):

    def build(self):
        return sm

    def load_app(self):
        sm.add_widget(AppWindow(name='app_app_screen'))
        sm.add_widget(HomeWindow(name='app_home_screen'))
    
    def unload_app(self):
        sm.remove_widget(AppWindow(name='app_app_screen'))
        sm.remove_widget(HomeWindow(name='app_home_screen'))

if __name__ == '__main__':
    MainApp().run()