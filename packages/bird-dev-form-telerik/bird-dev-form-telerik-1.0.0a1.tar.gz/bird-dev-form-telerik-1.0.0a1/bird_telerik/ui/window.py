from bird_telerik.ui.widget import BTWidget
from bird_form.windows.window import BFWindow


class BTWindow(BFWindow, BTWidget):
    def Init(self):
        from Telerik.WinControls.UI import RadForm
        self._ = RadForm()