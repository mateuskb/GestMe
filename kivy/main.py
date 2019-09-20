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
from pages.app.update_perfil.uperfil import UperfilWindow


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

        
class MainApp(App):

    def build(self):
        self.load_launcher()
        return sm
    
    def clear_widgets(self, screens=None):
        if screens is None:
            screens = sm.screens

        for screen in screens[:]:
            sm.remove_widget(screen)

    def load_launcher(self):
        sm.add_widget(GestMeWindow(name='gestme_screen'))
        sm.add_widget(LogInWindow(name='login_screen'))
        sm.add_widget(SignUpWindow(name='signup_screen'))
        sm.add_widget(SignupokWindow(name='signupok_screen'))
        # print("Load_pages : ", sm.screens)

    def load_app(self):
        sm.add_widget(AppWindow(name='app_app_screen'))
        sm.add_widget(HomeWindow(name='app_home_screen'))
        sm.add_widget(UperfilWindow(name='app_uperfil_screen'))
        # print("Load_app : ", sm.screens)

    def unload_app(self):
        self.clear_widgets()
        self.load_launcher()
        # print("Unload : ", sm.screens)
    

if __name__ == '__main__':
    MainApp().run()