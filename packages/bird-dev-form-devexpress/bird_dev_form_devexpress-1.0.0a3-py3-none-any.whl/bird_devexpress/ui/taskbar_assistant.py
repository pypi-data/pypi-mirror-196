from DevExpress.Utils.Taskbar import TaskbarAssistant
from DevExpress.Utils.Taskbar.Core import TaskbarButtonProgressMode
from bird import BObject


BDTaskBarButtonProgressMode = TaskbarButtonProgressMode


class BDTaskBarAssistant(BObject):
    def Init(self):
        self._ = TaskbarAssistant()

    def SetProgressValue(self, Value: int):
        self._.ProgressCurrentValue = Value

    def GetProgressValue(self):
        return self._.ProgressCurrentValue

    def SetProgressMode(self, Mode):
        self._.ProgressMode = Mode