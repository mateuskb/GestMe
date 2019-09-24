import sys, os, webbrowser
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.clock import Clock
import pandas as pd

BASE_PATH = os.path.abspath(__file__+ '/../../../../')

sys.path.append(BASE_PATH)
from inc.classes.Buttons import HoverButton, ImageButton
from inc.classes.Requests import Requests
from inc.classes.Storage import Storage
from inc.consts.consts import Consts


# Load KV file
Builder.load_file(BASE_PATH + '/pages/app/update_perfil/uperfil.kv')


class UperfilWindow(Screen):

    avatar = BASE_PATH + '/inc/assets/avatars/default.png'

    def __init__(self, **kwargs):
        super(UperfilWindow, self).__init__(**kwargs)
        # Check for login
        self.auth_token = Storage.r_authtoken()
        if not self.auth_token:
            Clock.schedule_once(self.logout, 2/30)
        else:
            Clock.schedule_once(self.load_profile, 3/30)
        
    def load_profile(self, dt):
        resp = Requests.r_perfil()
        if resp:
            if resp['status'] == 200:
                perfil = resp['data'] if 'data' in resp else []
                
            else:
                self.logout()
        else:
            self.logout()
        
    def consts(self):
        return Consts()
        
    def redirect_app_home(self):
        self.parent.current = 'app_home_screen'
    
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
                                                        self.parent.current = 'signupok_screen'
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
    
    def logout(self):
        resp = Storage.logoff()
        if resp:
            App.get_running_app().unload_app()


class UperfilApp(App):

    def build(self):
        return UperfilWindow()

if __name__ == '__main__':
    UperfilApp().run()
