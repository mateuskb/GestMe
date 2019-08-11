import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder

sys.path.append('../../')
from inc.Classes.Requests import Requests
from inc.consts.consts import Consts

# Load KV file
Builder.load_file('pages/signup/signup.kv')

class SignUpWindow(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def consts(self):
        return Consts()

    def redirect_gestme(self):
        self.parent.parent.current = 'gestme_screen'
    
    def validate_user(self):
        pass
    
    def list_formacoes(self):
        info = self.ids.info
        resp = Requests.r_formacoes()
        lista = ()
        if resp:
            if resp['status'] == 200:
                for item in resp['data']:
                    lista = lista + (item['for_c_formacao'], )
                return lista
            else:
                info.text = 'Connection lost, try again later!'
                return lista
        else:
            info.text = 'Connection lost, try again later!'
            return lista

class SignUpApp(App):

    def build(self):
        return SignUpWindow()

if __name__ == '__main__':
    SignUpApp().run()