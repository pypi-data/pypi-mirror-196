from bird_devexpress.ui.widget import BDWidget
from bird_form.windows.window import BFWindow


class BDWindow(BFWindow, BDWidget):
    def Init(self):
        from DevExpress.XtraEditors import XtraForm
        self._ = XtraForm()