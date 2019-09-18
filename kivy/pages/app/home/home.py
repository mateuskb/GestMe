import sys, os, webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
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

    avatar = BASE_PATH + '/inc/assets/avatars/default.png'

    default_image = BASE_PATH + '/inc/assets/movie_bck_default.jpg'

    def __init__(self, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        # Check for login
        self.auth_token = Storage.r_authtoken()
        if not self.auth_token:
            Clock.schedule_once(self.logout, 2/30)
        else:
            Clock.schedule_once(self.load_movies, 3/30)
            Clock.schedule_once(self.load_profile, 3/30)
        

    def load_movies(self, dt):
        menuTab = TabbedPanelHeader(text="Movies", background_color=Consts().COLOR_APP[1], background_down="")
        self.ids.tabs_home.add_widget(menuTab)
        sv = ScrollView()
        menuTab.content = sv
        container = GridLayout(cols=10, row_default_height=200, col_default_width=10)
        sv.add_widget(container)

        for index, row in self.mv_data.iterrows():
            if 'con_c_image_path' in row:
                if row['con_c_image_path']:
                    container.add_widget(ImageButton(id=str(index), source=Consts.BASE_IMAGE_MOVIE_URL + row['con_c_image_path'], size_hint_x=None, on_release=self.image_press))
                    # a.bind(on_press=self.image_press(0))
                else:
                    container.add_widget(ImageButton(source=self.default_image, size_hint_x=None))
            else:
                container.add_widget(ImageButton(source=self.default_image, size_hint_x=None))
            
    def load_profile(self, dt):
        resp = Requests.r_perfil(self.auth_token)
        if resp:
            if resp['status'] == 200:
                perfil = resp['data'] if 'data' in resp else []
                if perfil:
                    if 'per_c_perfil' in perfil:
                        self.ids.name_label.text = perfil['per_c_perfil']
                        
                    if 'per_c_avatar' in perfil:
                        try:
                            open(BASE_PATH + '/inc/assets/avatars' + perfil['per_c_avatar'])
                            self.ids.avatar_img.source = BASE_PATH + '/inc/assets/avatars' + perfil['per_c_avatar']
                        except:
                            self.ids.avatar_img.source = avatar

                else:
                    pass # Recommendation Page to do
            else:
                self.logout()
        else:
            self.logout()

    def consts(self):
        return Consts()

    def image_press(self, object):  
        link = self.mv_data.iloc[int(object.id)]['con_c_link']
        if link:
            webbrowser.open(link)
        
    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()


class HomeApp(App):

    def build(self):
        return HomeWindow()

if __name__ == '__main__':
    HomeApp().run()
