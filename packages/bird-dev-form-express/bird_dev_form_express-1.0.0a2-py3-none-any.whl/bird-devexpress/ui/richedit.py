from bird_form.windows.button import BFButton
from bird_devexpress.ui.widget import BDWidget


class BDRichEdit(BDWidget):
    def __init__(self, Text: str = ""):
        super().__init__()
        self.SetText(Text)

    def Init(self):
        from DevExpress.XtraRichEdit import RichEditControl
        self._ = RichEditControl()

    def SetText(self, Text: str):
        self._.Text = Text

    def GetText(self):
        return self._.Text