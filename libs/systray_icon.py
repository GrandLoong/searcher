from PySide import QtCore, QtGui
import config


class SearcherSystemTrayIcon(QtGui.QSystemTrayIcon):
    """ wrapper around system tray resources """

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setToolTip('searcher')
        self.activated.connect(self.icon_activated)
        self.gui_show = True
        self.parent = parent
        self.desktop = QtGui.QDesktopWidget()
        self.center()
        self.iconComboBox = QtGui.QComboBox()
        self.iconComboBox.addItem(QtGui.QIcon(config.add_icon('icon_256.png')), "Dmyz")
        self.quitAction = QtGui.QAction("exit", self, triggered=QtGui.qApp.quit)
        self.showAction = QtGui.QAction("open", self, triggered=self.show)
        self.quitAction.setShortcut("Ctrl+Q")
        self.trayIconMenu = QtGui.QMenu(self.parent)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIconMenu.addAction(self.showAction)
        self.setContextMenu(self.trayIconMenu)
        self.iconComboBox.currentIndexChanged.connect(self.set_icon)
        self.iconComboBox.setCurrentIndex(1)



    def set_icon(self, index):
        icon = self.iconComboBox.itemIcon(0)
        self.setIcon(icon)
        self.parent.setWindowIcon(icon)
        self.setToolTip(self.iconComboBox.itemText(index))

    def center(self):
        qr = self.parent.frameGeometry()
        cp = self.desktop.availableGeometry().center()
        qr.moveCenter(cp)
        self.parent.move(qr.topLeft())

    def icon_activated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            if self.gui_show:
                # self.hide()
                self.parent.close()
                self.gui_show = False
            else:
                self.parent.show()
                self.center()
                self.gui_show = True
