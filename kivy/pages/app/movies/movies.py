import sys, os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
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

    mv_data = pd.read_csv(BASE_PATH + '/inc/test_data/20movies.csv') # TO DO
    mv_data = mv_data.where((pd.notnull(mv_data)), None)

    default_image = BASE_PATH + '/inc/assets/movie_bck_default.jpg'
   
    # images_urls = [
    #     StringProperty(None),
    #     StringProperty(None)
    # ]
    # a = 0
    # for image in images_urls:
    #     images_urls[a] = default_image  
    #     a += 1

    
    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        # Check for login
        auth_token = Storage.r_authtoken()
        if not auth_token:
            Clock.schedule_once(self.logout, 2/30)

        Clock.schedule_once(self.load_movies, 3/30)


    def load_movies(self, dt):
        print('a')
        layout = self.ids.grid_lay

        for index, row in self.mv_data.iterrows():
            if 'con_c_image_path' in row:
                if row['con_c_image_path']:
                    layout.add_widget(ImageButton(source=Consts.BASE_IMAGE_MOVIE_URL + row['con_c_image_path'], size_hint_x=None))
                    # a.bind(on_press=self.image_press(0))
                else:
                    layout.add_widget(ImageButton(source=self.default_image, size_hint_x=None))
            else:
                layout.add_widget(ImageButton(source=self.default_image, size_hint_x=None))
        
        # self.ids.image.reload()
        # self.ids.image.source = self.images_urls[0]
    
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
