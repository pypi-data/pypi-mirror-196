from bird_form.windows.button import BFButton
from bird_telerik.ui.widget import BTWidget


class BTButton(BFButton, BTWidget):
    def Init(self):
        from Telerik.WinControls.UI import RadButton
        self._ = RadButton()