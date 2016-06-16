# -*- coding: utf-8 -*-
import sys
from os.path import join as pathjoin

from PySide import QtGui, QtCore

import config
from libs.Core import Searchers
from libs.completer import CustomQCompleter
from libs.systray_icon import SearcherSystemTrayIcon
from ui_elements.loadui import loadUiType, loadStyleSheet

uiFile = pathjoin(config.APP_DIR, 'resources/searcher2.ui')
css_file = pathjoin(config.APP_DIR, 'resources/searcher.css')
completer_css = pathjoin(config.APP_DIR, 'resources/completer.css')
ui_form, ui_base = loadUiType(uiFile)


class SearcherGui(ui_form, ui_base):
    def __init__(self):
        super(SearcherGui, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.SubWindow)
        self.completer = CustomQCompleter(self)
        self.search_comboBox.setCompleter(self.completer)
        self.search_comboBox.returnPressed.connect(self.run)
        self.search_comboBox.textChanged.connect(self.change_completer)
        self.set_transparency(True)
        self.searchers = Searchers()
        self.trayIcon = SearcherSystemTrayIcon(self)
        self.trayIcon.show()

    def change_completer(self):
        text = self.search_comboBox.text()
        self.completer.chage_completer(text)

    def run(self):
        # if self.completer.currentCompletion():
        #     self.search_comboBox.setText(self.completer.currentCompletion())
        text = self.search_comboBox.text()
        print self.completer.completionRole()
        # print self.completer.completionPrefix()
        # print self.completer.currentCompletion()
        # self.completer.save_completer(text)
        self.searchers.run(text)

    def set_transparency(self, enabled):
        if enabled:
            self.setAutoFillBackground(False)
        else:
            self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, enabled)
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    gui = SearcherGui()
    gui.setStyleSheet(loadStyleSheet(css_file))
    gui.show()
    app.exec_()
