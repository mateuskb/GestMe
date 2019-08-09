import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

sys.path.append('../')
from request.Classes.Requests import Requests

class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def validade_user(self):
        username = self.ids.usr_field.text
        password = self.ids.pwd_field.text
        info = self.ids.info

        if username == '' or password == '':
            info.text = '[color=#ff0000]Username/Password Required[/color]'
        else:
            if not username.isalnum() or not password.isalnum():
                info.text = '[color=#ff0000]Username/Password invalid[/color]'
            else:
                pass

class SigninApp(App):

    def build(self):
        return SigninWindow()

if __name__ == '__main__':
    SigninApp().run()