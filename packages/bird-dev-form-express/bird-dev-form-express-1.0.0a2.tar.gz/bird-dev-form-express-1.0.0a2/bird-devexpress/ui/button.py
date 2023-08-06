from bird_form.windows.button import BFButton
from bird_devexpress.ui.widget import BDWidget


class BDButton(BFButton, BDWidget):
    def Init(self):
        from DevExpress.XtraEditors import SimpleButton
        self._ = SimpleButton()
