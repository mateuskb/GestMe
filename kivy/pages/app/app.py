import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock


BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/app.kv')

class AppWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check for login
        auth_token = Storage.r_authtoken()
        print(auth_token)
        if not auth_token:
            self.logout()
        else:
            resp = Requests.r_perfil(auth_token)
            if resp:
                if resp['status'] == 200:
                    perfil = resp['data'] if 'data' in resp else {}
                    if perfil:
                        email_auth = perfil['per_b_email_auth'] if 'per_b_email_auth' in perfil else False
                        ativo = perfil['per_b_ativo'] if 'per_b_ativo' in perfil else False
                        if ativo:
                            if email_auth:
                                resp = Requests.r_historico_perfil(auth_token)
                                if resp:
                                    if resp['status'] == 200:
                                        historico = resp['data'] if 'data' in resp else []
                                        if historico:
                                            Clock.schedule_once(self.redirect_app_home, 1/60)
                                        else:
                                            pass # Recommendation Page to do
                                    else:
                                        self.logout()
                                else:
                                    self.logout()
                            else:
                                pass # Email auth page TO DO
                        else:
                            self.logout()
                    else:
                        self.logout()
                else:
                    self.logout()
            else:
                self.logout()


    def redirect_app_home(self, dt):
        self.parent.parent.current = 'app_home_screen'

    def logout(self):
        resp = Storage.logoff()
        if resp:
            self.parent.parent.current = 'gestme_screen'


class AppApp(App):

    def build(self):
        return AppWindow()

if __name__ == '__main__':
    AppApp().run()
