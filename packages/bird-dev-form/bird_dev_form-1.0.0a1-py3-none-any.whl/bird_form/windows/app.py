from bird.object import BObject


class BFApplication(BObject):
    def Init(self):
        from System.Windows.Forms import Application
        self._ = Application()

    def BindExit(self, Func):
        self._.ApplicationExit += Func

    def Run(self, Window):
        self._.Run(Window.Get())

    def Restart(self):
        self._.Restart()

    def Exit(self):
        self._.Exit()
