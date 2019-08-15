import sys, os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.core.window import Window

BASE_PATH = os.path.abspath(__file__+ '/../../../')

sys.path.append(BASE_PATH)

from inc.classes.Requests import Requests
from inc.classes.DateInput import DateInput
from inc.consts.consts import Consts

# Load KV file
Builder.load_file(BASE_PATH + '/pages/signup/signup.kv')

class SignUpWindow(BoxLayout):

    Window.size = (1100, 700)

    DateInput = DateInput()

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
        birthday = self.ids.bir_field.text
        password = self.ids.pwd_field.text
        confirmation = self.ids.vpw_field.text
        formacao = self.ids.fom_field.text
        pais = self.ids.pai_field.text
        info = self.ids.info

        error_invalid = '[color=#ff0000]Invalid inputs[/color]'
        error_password = '[color=#ff0000]Confirm password does not match[/color]'
        error_required = '[color=#ff0000]Inputs Required[/color]'
        error_server = '[color=#ff0000]Connection lost! Try again later![/color]'

        if name == '' or username == '' or email == '' or birthday == '' or password == '' or confirmation == '' or formacao == 'Education' or pais == 'Contries':
            info.text = error_required
        else:
            if password != confirmation:
                info.text = error_password
            else:
                if len(birthday) != 10:
                    info.text = error_invalid
                else:
                    # birthday = datetime.strptime(birthday, '%d/%m/%Y')
                    resp = Requests.r_formacao_nome(formacao)
                    if resp:
                        if resp['data']:
                            if 'for_pk' in resp['data']:
                                formacao = resp['data']['for_pk']
                                resp = Requests.r_pais_nome(pais)
                                if resp:
                                    if resp['data']:
                                        if 'pai_pk' in resp['data']:
                                            pais = resp['data']['pai_pk']
                                            resp = Requests.c_perfil(name, username, email, password, birthday, pais, formacao)
                                            if resp:
                                                if resp['ok']:
                                                    if resp['data']:
                                                        self.clear_inputs()
                                                        self.parent.parent.current = 'signupok_screen'
                                                    else:
                                                        for error in resp['errors'].values():
                                                            info.text = info.text + f'{error} \n'  
                                                else:
                                                    for error in resp['errors'].values():
                                                        info.text = info.text + f'{error} \n'  
                                            else:
                                                info.text = error_server
                                        else:
                                            info.text = error_server
                                    else:
                                        info.text = error_server
                                else:
                                    info.text = error_server
                            else:
                                info.text = error_server
                        else:
                            info.text = error_server
                    else:
                        info.text = error_server    
                        

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
                    lista = lista + (item['pai_c_pais'], )
                return lista
            else:
                info.text = 'Connection lost, try again later!'
                return lista
        else:
            info.text = 'Connection lost, try again later!'
            return lista
    
    def clear_inputs(self):
        self.ids.nam_field.text = ''
        self.ids.usr_field.text = ''
        self.ids.ema_field.text = ''
        self.ids.bir_field.text = ''
        self.ids.pwd_field.text = ''
        self.ids.vpw_field.text = ''
        self.ids.fom_field.text = 'Education'
        self.ids.pai_field.text = 'Contries'
        self.ids.info.text = ''

class SignUpApp(App):

    def build(self):
        return SignUpWindow()

if __name__ == '__main__':
    SignUpApp().run()