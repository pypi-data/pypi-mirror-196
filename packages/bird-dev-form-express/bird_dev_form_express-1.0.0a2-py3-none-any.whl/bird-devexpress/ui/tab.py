from bird_form.windows.tab import BFTab
from bird_form.windows.panel import BFPanel
from bird_devexpress.ui.widget import BDWidget


class BDTabNavigationPage(BFPanel, BDWidget):
    def __init__(self, Caption: str):
        super().__init__()
        self.SetCaption(Caption)

    def Init(self):
        from DevExpress.XtraBars.Navigation import TabNavigationPage
        self._ = TabNavigationPage()

    def SetCaption(self, Text: str):
        self._.Caption = Text


class BDTabPane(BFTab, BDWidget):
    def Init(self):
        from DevExpress.XtraBars.Navigation import TabPane
        self._ = TabPane()


class BDTabPage(BFPanel, BDWidget):
    def Init(self):
        from DevExpress.XtraTab import XtraTabPage
        self._ = XtraTabPage()


class BDTab(BFTab, BDWidget):
    def Init(self):
        from DevExpress.XtraTab import XtraTabControl
        self._ = XtraTabControl()

    def TabAdd(self, Widget):
        self._.TabPages.AddRange(Widget.Get())