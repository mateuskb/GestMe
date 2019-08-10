import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

sys.path.append('../../')
from request.Classes.Requests import Requests

class GestMeWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GestMeApp(App):

    def build(self):
        return GestMeWindow()

if __name__ == '__main__':
    GestMeApp().run()