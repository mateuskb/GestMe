import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

sys.path.append('../../')
from request.Classes.Requests import Requests

class RegisterWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RegisterApp(App):

    def build(self):
        return RegisterWindow()

if __name__ == '__main__':
    RegisterApp().run()