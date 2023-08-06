from bird_form.windows.widget import BFWidget


class BFTab(BFWidget):
    def __init__(self):
        super().__init__()

    def Init(self):
        from System.Windows.Forms import TabControl
        self._ = TabControl()

    def PageAdd(self, Widget):
        self._.Pages.Add(Widget.Get())