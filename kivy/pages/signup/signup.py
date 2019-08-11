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
        name = self.ids.nam_field.text
        username = self.ids.usr_field.text
        email = self.ids.ema_field.text
        password = self.ids.pwd_field.text
        confirmation = self.ids.vpw_field.text
        formacao = self.ids.fom_field.text
        info = self.ids.info

        error_invalid = '[color=#ff0000]Username/Password invalid[/color]'
        error_required = '[color=#ff0000]Username/Password Required[/color]'

        # if username == '' or password == '':
        #     info.text = error_required
        # else:
        #     if not username.isalnum() or not password.isalnum():
        #         info.text = error_invalid
        info.text = formacao            
    

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
    
    def list_paises(self):
        info = self.ids.info
        resp = Requests.r_paises()
        lista = ()
        if resp:
            if resp['status'] == 200:
                for item in resp['data']:
                    lista = lista + (item['pai_c_pais'] + ' - ' + item['pai_c_cod'], )
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