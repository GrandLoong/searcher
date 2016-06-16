import os
import re
import _winreg
from PySide import QtCore, QtGui
import config


class CustomQCompleter(QtGui.QCompleter):
    DELIMITERS = r'[()\[\]*+-=/\\]'

    def __init__(self, *args):
        QtGui.QCompleter.__init__(self, *args)
        self.setModel(QtGui.QDirModel(self))
        self.local_completion_prefix = ''
        self.source_model = None
        self.filterProxyModel = QtGui.QSortFilterProxyModel(self)


    def updateModel(self):
        pattern = QtCore.QRegExp(self.local_completion_prefix, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
        self.filterProxyModel.setFilterRegExp(pattern)



    # def setModel(self):


    def set_completer(self):
        # self.setCompletionMode(0)
        self.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        # self.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        self.setModel(QtGui.QDirModel(self))
        # self.setModel(self.modelFromFile(config.normpath(config.APP_DIR, 'resources/list.txt')))
        self.setModelSorting(QtGui.QCompleter.CaseInsensitivelySortedModel)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setMaxVisibleItems(20)
        self.setWrapAround(False)

    def chage_completer(self, data):
        if re.match('(\w):.+', data):
            self.setModel(QtGui.QDirModel(self))
        if os.path.isdir(data):
            self.setModel(QtGui.QDirModel(self))
        else:
            self.setModel(self.modelFromFile(config.normpath(config.APP_DIR, 'resources/list.txt')))

    @staticmethod
    def get_local_completer():
        local_dir = config.get_local_profile_dir()
        completer_file = config.normpath(local_dir, 'completer.txt')
        if os.path.isfile(completer_file):
            words = []
            with open(completer_file, 'r') as f:
                lines = f.readlines()
            if lines:
                for line in lines:
                    words.append(line.strip('\n'))
            return words


    @staticmethod
    def save_completer(text):
        local_dir = config.get_local_profile_dir()
        completer_file = config.normpath(local_dir, 'completer.txt')
        with open(completer_file, 'a') as f:
            f.write(text + '\n')


    @staticmethod
    def get_gloacl_completer():
        completer_file = config.normpath(config.APP_DIR, 'resources/list.txt')
        words = []
        c = []
        dics = {}
        with open(completer_file, 'r') as f:
            lines = f.readlines()
        if lines:
            for line in lines:
                dirs = os.listdir(line.strip('\n'))
                for d in dirs:
                    c.append(d)
                    dics[d] = config.normpath(line, d)
        return c

    @staticmethod
    def get_runmru_completer():
        completers = []
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU")

        try:
            i = 0

            while 1:
                name, value, type = _winreg.EnumValue(key, i)
                completers.append(value.strip('\\1'))
                i += 1
        except WindowsError:
            pass
        return completers
            #
    def modelFromFile(self,fileName):
        # f = QtCore.QFile(fileName)
        # if not f.open(QtCore.QFile.ReadOnly):
        #     return QtGui.QStringListModel(self.completer)

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        data = self.build_completer()

        QtGui.QApplication.restoreOverrideCursor()
        return QtGui.QStringListModel(data, self)
            #
    def build_completer(self):
        global_data = self.get_gloacl_completer()
        local_data = self.get_local_completer()
        run_data = self.get_runmru_completer()
        if run_data:
            global_data.extend(run_data)
        if local_data:
            global_data.extend(local_data)

        return global_data
