from clr import AddReference
from bird import BObject
from bird_telerik import (telerik_wincontrols_win11_lib, telerik_wincontrols_office2013_light_lib,
                          telerik_wincontrols_office2013_dark_lib, telerik_wincontrols_vs2012_light_lib,
                          telerik_wincontrols_vs2012_dark_lib)


class BTWindows11Theme(BObject):
    def Init(self):
        AddReference(telerik_wincontrols_win11_lib)
        from Telerik.WinControls.Themes import Windows11Theme
        self._ = Windows11Theme()

    def __str__(self):
        return "Windows11"


class BTOffice2013Theme(BObject):
    def Init(self):
        AddReference(telerik_wincontrols_office2013_light_lib)
        from Telerik.WinControls.Themes import Office2013LightTheme
        self._ = Office2013LightTheme()

    def __str__(self):
        return "Office2013Light"


class BTOffice2013DarkTheme(BObject):
    def Init(self):
        AddReference(telerik_wincontrols_office2013_dark_lib)
        from Telerik.WinControls.Themes import Office2013DarkTheme
        self._ = Office2013DarkTheme()

    def __str__(self):
        return "Office2013Dark"


class BTVS2012Theme(BObject):
    def Init(self):
        AddReference(telerik_wincontrols_vs2012_light_lib)
        from Telerik.WinControls.Themes import VisualStudio2012LightTheme
        self._ = VisualStudio2012LightTheme()

    def __str__(self):
        return "VisualStudio2012Light"


class BTVS2012DarkTheme(BObject):
    def Init(self):
        AddReference(telerik_wincontrols_vs2012_dark_lib)
        from Telerik.WinControls.Themes import VisualStudio2012DarkTheme
        self._ = VisualStudio2012DarkTheme()

    def __str__(self):
        return "VisualStudio2012Darl"