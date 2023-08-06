from bird_form.windows.panel import BFPanel
from bird_devexpress.ui.widget import BDWidget


class BDPanel(BFPanel, BDWidget):
    def Init(self):
        from DevExpress.XtraEditors import PanelControl
        self._ = PanelControl()