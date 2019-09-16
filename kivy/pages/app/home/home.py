import sys, os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
import pandas as pd

BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Buttons import HoverButton, ImageButton
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts


# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/home/home.kv')


class HomeWindow(Screen):

    mv_data = pd.read_csv(BASE_PATH + '/inc/test_data/20movies.csv')[:2]
    default_image = BASE_PATH + '/inc/data/assets/movie_bck_default.jpg'
    base_path = 'http://image.tmdb.org/t/p/w185'
    images_urls = [
        StringProperty(None),
        StringProperty(None)
    ]
    a = 0
    for image in images_urls:
        images_urls[a] = default_image  
        a += 1

    
    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        # Check for login
        auth_token = Storage.r_authtoken()
        if not auth_token:
            Clock.schedule_once(self.logout, 2/30)

        # Clock.schedule_once(self.load_movies, 2/30)


    def load_movies(self, dt):
        for index, row in self.mv_data.iterrows():
            self.images_urls[index] = self.base_path + row['con_c_image_path']
        
        self.ids.image.reload()
        print(self.images_urls)
    
    def consts(self):
        return Consts()

    def image_press(self, id):  
        print ('pressed ', id)

    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
