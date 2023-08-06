from bird_form.windows.widget import BFWidget


class BFPanel(BFWidget):
    def __init__(self):
        super().__init__()

    def Init(self):
        from System.Windows.Forms import Panel
        self._ = Panel()
