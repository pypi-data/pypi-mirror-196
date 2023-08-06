from bird_form.windows.button import BFButton
from bird_devexpress.ui.widget import BDWidget


class BDToggleSwitch(BFButton, BDWidget):
    def __init__(self, Text: str = ""):
        super().__init__(Text=Text)

    def Init(self):
        from DevExpress.XtraEditors import ToggleSwitch
        self._ = ToggleSwitch()

    def SetOn(self, On: bool):
        self._.IsOn = On

    def IsOn(self):
        return self._.IsOn

    def BindToggle(self, Func):
        self._.Toggled += Func