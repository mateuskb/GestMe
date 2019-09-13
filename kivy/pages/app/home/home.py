import sys, os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty


BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/home/home.kv')

# class FullImage(Image):
#         pass


class HomeWindow(Screen):

    base_path = 'http://image.tmdb.org/t/p/w185/'
    image_path = base_path + '16XOMpEaLWkrcPqSQqhTmeJuqQl.jpg'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check for login
        resp = Storage.r_authtoken()
        if not resp:
            self.logout()   

    def consts(self):
        return Consts()
    
    def change_image(self, path):
        self.image_path = self.base_path + path
        print( self.image_path)

    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()        


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
