import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen

BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/home/home.kv')

class HomeWindow(Screen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check for login
        resp = Storage.r_authtoken()
        if not resp:
            self.logout()   
        

    def consts(self):
        return Consts()
    
    def logout(self):
        resp = Storage.logoff()
        if resp:
            self.parent.current = 'gestme_screen'


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
