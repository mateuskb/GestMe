import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.consts.consts import Consts
from inc.classes.Buttons import HoverButton, FlatButton
# from pages.app.app import AppWindow

# Load KV file
Builder.load_file(BASE_PATH + '/pages/login/login.kv')

class LogInWindow(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def consts(self):
        return Consts()

    def validate_user(self):
        username = self.ids.usr_field.text
        password = self.ids.pwd_field.text
        info = self.ids.info
        storage = JsonStore(Consts.JSON_PATH)

        error_invalid = '[color=#ff0000]Username/Password invalid[/color]'
        error_required = '[color=#ff0000]Username/Password Required[/color]'

        if username == '' or password == '':
            info.text = error_required
        else:
            if not username.isalnum() or not password.isalnum():
                info.text = error_invalid
            else:
                resp = Requests.login(username, password)
                if resp:
                    if resp['status'] == 200:
                        if resp['data']:
                            storage['login'] = {'authToken': resp['data']}
                            self.redirect_app()
                    elif resp['status'] == 401:
                        info.text = error_invalid
                    else:
                        info.text = error_invalid
                else:
                    info.text = 'Connection lost, try again later!'

    def redirect_gestme(self):
        self.clear_inputs()
        self.parent.current = 'gestme_screen'

    def redirect_app(self):
        self.clear_inputs()
        # self.parent.switch_to(AppWindow(name='app_app_screen'))
        App.get_running_app().load_app()
        self.parent.current = 'app_app_screen'


    def redirect_forgetpw(self):
        pass

    def clear_inputs(self):
        self.ids.pwd_field.text = ''


class LogInApp(App):

    def build(self):
        print('oi')
        return LogInWindow()

if __name__ == '__main__':
    LogInApp().run()
