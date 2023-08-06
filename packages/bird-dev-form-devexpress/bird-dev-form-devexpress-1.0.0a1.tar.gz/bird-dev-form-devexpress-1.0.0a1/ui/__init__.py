from clr import AddReference
from bird_devexpress import (devexpress_xtra_bars, devexpress_xtra_editors, devexpress_bonus_skins, devexpress_utils,
                             devexpress_xtra_richedit)

AddReference(devexpress_utils)
AddReference(devexpress_xtra_bars)
AddReference(devexpress_xtra_editors)
AddReference(devexpress_xtra_richedit)
AddReference(devexpress_bonus_skins)

from bird_devexpress.ui.widget import BDWidget
from bird_devexpress.ui.window import BDWindow
from bird_devexpress.ui.fluentwindow import BDFluentWindow, BDFluentWindowContainer, BDFluentWindowWidget
from bird_devexpress.ui.button import BDButton
from bird_devexpress.ui.toggle import BDToggleSwitch
from bird_devexpress.ui.richedit import BDRichEdit
from bird_devexpress.ui.style import BDStyle
from bird_devexpress.ui.settings import BDUseDirectX
from bird_devexpress.ui.taskbar_assistant import BDTaskBarAssistant, BDTaskBarButtonProgressMode
from bird_devexpress.ui.panel import BDPanel
from bird_devexpress.ui.tab import BDTab, BDTabNavigationPage, BDTabPane, BDTabPage