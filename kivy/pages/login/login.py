import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

sys.path.append('../../')
from inc.Classes.Requests import Requests
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
        info = self.ids.info.text

        error_invalid = '[color=#ff0000]Username/Password invalid[/color]'
        error_required = '[color=#ff0000]Username/Password Required[/color]'

        if username == '' or password == '':
            info = error_required
        else:
            if not username.isalnum() or not password.isalnum():
                info = error_invalid
            else:
                resp = Requests.login(username, password)
                if resp['status'] == 200:
                    info = 'Login Success!'
                elif resp['status'] == 401:
                    info = error_invalid
                else:
                    info = error_invalid
    
    def redirect_gestme(self):
        self.parent.parent.current = 'gestme_screen'
    
    def redirect_forgetpw(self):
        pass


class LogInApp(App):

    def build(self):
        return LogInWindow()

if __name__ == '__main__':
    LogInApp().run()
