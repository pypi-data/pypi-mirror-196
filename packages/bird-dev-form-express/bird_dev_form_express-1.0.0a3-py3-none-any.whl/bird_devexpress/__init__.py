import os
lib = os.path.dirname(__file__).replace("\\", "//")

devexpress_utils = lib + "//ui//DevExpress.Utils.v22.2.dll"

devexpress_xtra_bars = lib + "//ui//DevExpress.XtraBars.v22.2.dll"
devexpress_xtra_editors = lib + "//ui//DevExpress.XtraEditors.v22.2.dll"
devexpress_xtra_richedit = lib + "//ui//DevExpress.XtraEditors.v22.2.dll"

devexpress_bonus_skins = lib + "//ui//DevExpress.BonusSkins.v22.2.dll"


from bird_devexpress.ui import *
