import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore

BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/home/home.kv')

class HomeWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check authToken
        resp = Storage.r_authtoken()
        print(resp)
    
    def consts(self):
        return Consts()
    
    def redirect_gestme(self):
        self.parent.parent.current = 'gestme_screen'
    
    def redirect_forgetpw(self):
        pass


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
