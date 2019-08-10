import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

sys.path.append('../../')
from request.Classes.Requests import Requests
from consts.consts import Consts

# Load KV file
Builder.load_file('pages/login/login.kv')

class LogInWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def consts(self):
        return Consts()
        
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
                resp = Requests.login(username, password)
                if resp:
                    if resp['status'] == 200:
                        info.text = 'Login Success!'
                    elif resp['status'] == 401:
                        info.text = 'Anauthorized'
                    else:
                        info.text = '[color=#ff0000]Username/Password invalid[/color]'
                else:
                    info.text = '[color=#ff0000]Conection Lost! Try again later![/color]'

class LogInApp(App):

    def build(self):
        return LogInWindow()

if __name__ == '__main__':
    LogInApp().run()