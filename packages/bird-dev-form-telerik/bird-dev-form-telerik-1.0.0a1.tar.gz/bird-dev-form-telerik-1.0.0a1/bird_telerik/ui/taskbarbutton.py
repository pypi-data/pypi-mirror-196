from bird_form.windows.widget import BFWidget


class BTTaskBarButton(BFWidget):
    def Init(self):
        from Telerik.WinControls.UI import RadTaskbarButton
        self._ = RadTaskbarButton()

    def Add(self, Button):
        self._.ThumbnailButtons.Add(Button.Get())

    def OwnerWindow(self, Window):
        self._.OwnerForm = Window.Get()