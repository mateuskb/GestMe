import sys, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore

BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/home/home.kv')

class AppWindow(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check for login
        auth_token = Storage.r_authtoken()
        if not auth_token:
            self.logout()
        else:
            resp = Requests.r_historico_perfil(auth_token)
            if resp:
                historico = resp['data'] if 'data' in resp else []
                if historico:
                    print(historico)
                else:
                    pass # Recommendation page
            else:
                self.logout()


    # def logout(self):
    #     resp = Storage.logoff()
    #     if resp:
    #         self.parent.parent.current = 'gestme_screen'


class AppApp(App):

    def build(self):
        return AppWindow()

if __name__ == '__main__':
    AppApp().run()
