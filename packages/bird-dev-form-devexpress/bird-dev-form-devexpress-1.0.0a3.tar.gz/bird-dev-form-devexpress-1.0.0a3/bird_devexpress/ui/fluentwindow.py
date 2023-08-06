from bird_devexpress.ui.window import BDWindow
from bird_devexpress.ui.panel import BDPanel
from bird_devexpress.ui.widget import BDWidget


class BDFluentWindow(BDWindow):
    def Init(self):
        from DevExpress.XtraBars.FluentDesignSystem import FluentDesignForm
        self._ = FluentDesignForm()


class BDFluentWindowContainer(BDPanel):
    def Init(self):
        from DevExpress.XtraBars.FluentDesignSystem import FluentDesignFormContainer
        self._ = FluentDesignFormContainer()


class BDFluentWindowWidget(BDWidget):
    def Init(self):
        from DevExpress.XtraBars.FluentDesignSystem import FluentDesignFormControl
        self._ = FluentDesignFormControl()

    def FluentWindow(self, Window: BDFluentWindow):
        self._.FluentDesignForm = Window.Get()