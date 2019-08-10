import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

sys.path.append('../../')
from request.Classes.Requests import Requests
from consts.consts import Consts

class SignUpWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def consts(self):
        return Consts()


class SignUpApp(App):

    def build(self):
        return SignUpWindow()

if __name__ == '__main__':
    SignUpApp().run()