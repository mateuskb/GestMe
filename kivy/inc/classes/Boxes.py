import re, os
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior  
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.label import Label


BASE_PATH = os.path.abspath(__file__+ '/../../')

from inc.classes.Buttons import HoverBehavior

class HoverBox(HoverBehavior, BoxLayout):
    pass    