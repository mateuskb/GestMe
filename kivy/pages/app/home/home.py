import sys, os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
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

    # mv_data = pd.read_csv(BASE_PATH + '/inc/test_data/20movies.csv')[:1]
    # base_path = 'http://image.tmdb.org/t/p/w185'
    # images_urls = [
    #     StringProperty(''),
    #     StringProperty('')
    # ]
    # a = 0
    # for image in images_urls:
    #     images_urls[a] = 'http:/image.tmdb.org/t/p/w185/A3aYGp8LLxuFdzG2ETnhfbWPk7h.jpg'  
    #     a += 1

    # image_url = StringProperty('http:/image.tmdb.org/t/p/w185/A3aYGp8LLxuFdzG2ETnhfbWPk7h.jpg')
    
    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        # Check for login
        resp = Storage.r_authtoken()
        if not auth_token:
            Clock.schedule_once(self.logout, 2/30)
        # self.add_widget(ImageButton(source='http:/image.tmdb.org/t/p/w185/A3aYGp8LLxuFdzG2ETnhfbWPk7h.jpg'))
        # self.load_movies()

    # def load_movies(self):
    #     for index, row in self.mv_data.iterrows():
    #         self.images_urls[index] = self.base_path + row['con_c_image_path']
    
    def consts(self):
        return Consts()

    def on_press(self):  
        print ('pressed')

    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
