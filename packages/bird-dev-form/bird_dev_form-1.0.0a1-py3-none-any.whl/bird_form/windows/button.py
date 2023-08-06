from bird_form.windows.widget import BFWidget


class BFButton(BFWidget):
    def __init__(self, Text: str = ""):
        super().__init__()

        self.SetText(Text)

    def Init(self):
        from System.Windows.Forms import Button
        self._ = Button()

    def SetText(self, Text: str):
        self._.Text = Text

    def GetText(self):
        return self._.Text