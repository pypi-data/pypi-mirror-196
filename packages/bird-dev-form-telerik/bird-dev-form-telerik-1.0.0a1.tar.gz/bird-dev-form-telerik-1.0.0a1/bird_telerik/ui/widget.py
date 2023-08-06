from bird_form import BFWidget


class BTWidget(BFWidget):
    def SetThemeName(self, Theme: str):
        self._.ThemeName = Theme

    def GetThemeName(self):
        return self._.ThemeName