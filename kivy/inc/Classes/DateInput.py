import re
from kivy.uix.textinput import TextInput

class DateInput(TextInput):
    def keyboard_on_key_up(self, window, keycode):
        if keycode[1] == "backspace" and len(self.text) >= 1:
            if self.text[-1] == "/":
                self.text = self.text[:-1]
            else:
                pass
        else:
            pass
        TextInput.keyboard_on_key_up(self, window, keycode)

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if len(substring) > 1:
            substring = re.sub(pat, '', (self.text + substring))
            self.text = ''
            slen = len(substring)
            if slen == 2:
                s = substring[:2] + '/'
            elif slen == 3:
                s = substring[:2] + '/' + substring[2:]
            elif slen == 4:
                s = substring[:2] + '/' + substring[2:] + '/'
            else:
                s = substring[:2] + '/' + substring[2:4] + '/' + substring[4:8]
        elif len(self.text) > 9:
            s = ''
        elif len(self.text) == 2:
            s = re.sub(pat, '', substring)
            if s != '':
                s = '/' + s
        elif len(self.text) == 5:
            s = re.sub(pat, '', substring)
            if s != '':
                s = '/' + s
        else:
            s = re.sub(pat, '', substring)
        return super(DateInput, self).insert_text(s, from_undo=from_undo)