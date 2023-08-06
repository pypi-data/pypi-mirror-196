import os
lib = os.path.dirname(__file__).replace("\\", "//")

telerik_wincontrols_lib = lib + "//ui//Telerik.WinControls.dll"
telerik_wincontrols_ui_lib = lib + "//ui//Telerik.WinControls.UI.dll"

telerik_wincontrols_win11_lib = lib + "//ui//Telerik.WinControls.Themes.Windows11.dll"
telerik_wincontrols_office2013_light_lib = lib + "//ui//Telerik.WinControls.Themes.Office2013Light.dll"
telerik_wincontrols_office2013_dark_lib = lib + "//ui//Telerik.WinControls.Themes.Office2013Dark.dll"
telerik_wincontrols_vs2012_light_lib = lib + "//ui//Telerik.WinControls.Themes.VisualStudio2012Light"
telerik_wincontrols_vs2012_dark_lib = lib + "//ui//Telerik.WinControls.Themes.VisualStudio2012Dark"

from bird_telerik.ui import *
