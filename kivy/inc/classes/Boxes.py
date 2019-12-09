import re, os
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior  
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.label import Label


BASE_PATH = os.path.abspath(__file__+ '/../../')

from inc.classes.Buttons import HoverBehavior

class HoverBox(HoverBehavior, BoxLayout):
    pass    

class RoundedBox(Widget):
    corners = ListProperty([0, 0, 0, 0])
    line_width = NumericProperty(1)
    resolution = NumericProperty(100)
    points = ListProperty([])

    def compute_points(self, *args):
        self.points = []

        a = - pi

        x = self.x + self.corners[0]
        y = self.y + self.corners[0]
        while a < - pi / 2.:
            a += pi / self.resolution
            self.points.extend([
                x + cos(a) * self.corners[0],
                y + sin(a) * self.corners[0]
                ])

        x = self.right - self.corners[1]
        y = self.y + self.corners[1]
        while a < 0:
            a += pi / self.resolution
            self.points.extend([
                x + cos(a) * self.corners[1],
                y + sin(a) * self.corners[1]
                ])

        x = self.right - self.corners[2]
        y = self.top - self.corners[2]
        while a < pi / 2.:
            a += pi / self.resolution
            self.points.extend([
                x + cos(a) * self.corners[2],
                y + sin(a) * self.corners[2]
                ])

        x = self.x + self.corners[3]
        y = self.top - self.corners[3]
        while a < pi:
            a += pi / self.resolution
            self.points.extend([
                x + cos(a) * self.corners[3],
                y + sin(a) * self.corners[3]
                ])

        self.points.extend(self.points[:2])