from bird_form.windows.widget import BFWidget


class BFWindow(BFWidget):
    def Init(self):
        from System.Windows.Forms import Form
        self._ = Form()