from bird.object import BObject


class BFWidget(BObject):
    def SetName(self, Name: str):
        self._.Name = Name

    def Show(self):
        self._.Show()

    def Hide(self):
        self._.Hide()

    def Resize(self, Width: float | int, Height: float | int):
        from System.Drawing import Size
        self._.Size = Size(Width, Height)

    def Move(self, X: float | int, Y: float | int):
        from System.Drawing import Point
        self._.Location = Point(X, Y)

    def Pack(self, Fill: str = None, Margin: dict = (3, 3, 3, 3), Padding: dict = (3, 3, 3, 3)):
        from System.Windows.Forms import Padding as pad

        if Fill is not None:
            self._.Dock = Fill
        self._.Margin = pad(Margin[0], Margin[1], Margin[2], Margin[3])
        self._.Padding = pad(Padding[0], Padding[1], Padding[2], Padding[3])

    def Place(self, X=0, Y=0, Width=100, Height=30, Fill: str = None):
        if Fill is not None:
            self._.Dock = Fill
        self.Resize(Width, Height)
        self.Move(X, Y)

    def Add(self, Widget):
        self._.Controls.Add(Widget.Get())

    def Remove(self, Widget):
        self._.Controls.Remove(Widget.Get())

    def Enabled(self, Enable: bool):
        self._.Enabled = Enable

    def BindClick(self, Func):
        self._.Click += Func

    def BindMouseClick(self, Func):
        self._.MouseClick += Func