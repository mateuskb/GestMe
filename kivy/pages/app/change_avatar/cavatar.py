import sys, os, webbrowser
from datetime import datetime
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
Builder.load_file(BASE_PATH + '/pages/app/change_avatar/cavatar.kv')


class CavatarWindow(Screen):

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
                self.perfil = resp['data'] if 'data' in resp else []
                self.default_inputs()
            else:
                self.logout()
        else:
            self.logout()
        
    def consts(self):
        return Consts()
        
    def redirect_app_home(self):
        self.default_inputs()
        self.parent.current = 'app_home_screen'
    
    def validate_user(self):
        name = self.ids.nam_field.text
        username = self.ids.usr_field.text
        birthday = self.ids.bir_field.text
        formacao = self.ids.fom_field.text
        pais = self.ids.pai_field.text
        info = self.ids.info

        error_invalid = '[color=#ff0000]Invalid inputs[/color]'
        error_required = '[color=#ff0000]Inputs Required[/color]'
        error_server = '[color=#ff0000]Connection lost! Try again later![/color]'
        update_ok = '[color=#33ff55]Update completed with success!!![/color]'

        if name == '' or username == '' or birthday == '' or formacao == 'Education' or pais == 'Contries':
            info.text = error_required
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
                                        resp = Requests.u_perfil(name, username, birthday, pais, formacao)
                                        if resp:
                                            if resp['ok']:
                                                if resp['data']:
                                                    self.default_inputs()
                                                    info.text = update_ok
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

    def default_inputs(self):
        resp = Requests.r_perfil()
        if resp:
            if resp['status'] == 200:
                perfil = resp['data'] if 'data' in resp else []
                id_formacao = perfil['per_fk_formacao'] if 'per_fk_formacao' in perfil else 0
                resp = Requests.r_formacao_id(id_formacao)
                if resp['ok'] and resp['data']:
                    formacao = resp['data']['for_c_formacao']
                else:
                    formacao = 'Education'

                id_pais = perfil['per_fk_pais'] if 'per_fk_pais' in perfil else 0
                resp = Requests.r_pais_id(id_pais)
                if resp['ok'] and resp['data']:
                    pais = resp['data']['pai_c_pais']
                else:
                    pais = 'Contries'

                birth = perfil['per_d_nascimento'] if 'per_d_nascimento' in perfil else '01/01/1970'
                # print(birth)
                # try:
                #     birth = datetime.strptime(birth, "%d-%m-%Y")
                # except Exception as e:
                #     print(e)
                #     birth = '01/01/1970'

                self.ids.nam_field.text = perfil['per_c_perfil'] if 'per_c_perfil' in perfil else ''
                self.ids.usr_field.text = perfil['per_c_username'] if 'per_c_username' in perfil else ''
                self.ids.bir_field.text = birth
                self.ids.fom_field.text = formacao
                self.ids.pai_field.text = pais
                self.ids.info.text = ''
            else:
                self.logout()
        else:
            self.logout()
        


class UperfilApp(App):

    def build(self):
        return UperfilWindow()

if __name__ == '__main__':
    UperfilApp().run()
