import os
import re
import _winreg
from PySide import QtCore, QtGui
import WebSearchers as web_api
import config


class CustomQCompleter(QtGui.QCompleter):
    DELIMITERS = r'[()\[\]*+-=/\\]'

    def __init__(self, *args):
        QtGui.QCompleter.__init__(self, *args)
        self.setModel(QtGui.QDirModel(self))
        self.local_completion_prefix = ''
        self.global_data = self.get_gloacl_completer()
        self.local_data = self.get_local_completer()
        self.run_data = self.get_runmru_completer()

        self.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.filterProxyModel = QtGui.QSortFilterProxyModel(self)
        self.set_completer()
        self.source_model = None
        self.build_completer()

    def file_model(self):
        data = self.widget().text()
        self.dirModel = QtGui.QFileSystemModel(self)
        self.dirModel.setRootPath(data)
        self.dirModel.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.dirModel.setNameFilterDisables(0)
        return self.dirModel

    def updateModel(self):
        pattern = QtCore.QRegExp(self.local_completion_prefix, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString)
        self.filterProxyModel.setFilterRegExp(pattern)

    # def updateModel(self):
    #     local_completion_prefix = self.local_completion_prefix
    #     class InnerProxyModel(QtGui.QSortFilterProxyModel):
    #         def filterAcceptsRow(self, sourceRow, sourceParent):
    #             index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
    #             searchStr = local_completion_prefix.lower()
    #             modelStr = self.sourceModel().data(index0,QtCore.Qt.DisplayRole)#.toString().toLower()
    #             print searchStr,' in ',modelStr, searchStr in modelStr
    #             return searchStr in modelStr
    #
    #
    #     proxy_model = InnerProxyModel()
    #
    #     proxy_model.setSourceModel(self.source_model)
    #
    #     super(CustomQCompleter, self).setModel(proxy_model)
    #     print 'match :',proxy_model.rowCount()


    # def splitPath(self, path):
    #     print path
    #     self.chage_completer(path)
    #     return ""

    def set_completer(self):
        # self.setCompletionMode(0)
        self.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        # self.setModel(self.dirModel)
        # self.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        # self.setModel(self.modelFromFile(config.normpath(config.APP_DIR, 'resources/list.txt')))
        self.setModelSorting(QtGui.QCompleter.CaseInsensitivelySortedModel)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setMaxVisibleItems(20)
        self.setWrapAround(False)

    def chage_completer(self, data):
        math_ = re.match('(?P<key>\w+|>) (?P<cmd>.+)', data)
        if re.match('(\w):.+', data):
            # self.dirModel.setRootPath(data)
            self.setModel(QtGui.QDirModel(self))
        elif re.match(r'(>.+)', data):
            self.setModel(QtGui.QStringListModel(self.get_cmd_completer(), self))
        elif math_:
            math_key = math_.groupdict()['key']
            print 'web_search/{0}'.format(math_key)
            item = config.get_regexp('web_search/{0}'.format(math_key))
            print item
            try:
                self.setModel(QtGui.QStringListModel(['Search in {0}'.format(item['name'])]))
            except:
                pass
        else:
            self.setModel(self.modelFromFile())

    def get_cmd_completer(self):
        return ['> {0}'.format(x).strip('.bat') for x in os.listdir(config.normpath(config.PLUGINS_DIR, 'cmd'))]

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

    def get_web_search_key(self):
        return config.get_regexp('web_search')


    @staticmethod
    def get_gloacl_completer():
        completer_file = config.normpath(config.APP_DIR, 'resources/list.txt')
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
                name, value, type_ = _winreg.EnumValue(key, i)
                completers.append(value.strip('\\1'))
                i += 1
        except WindowsError:
            pass
        return completers
        #

    def modelFromFile(self):
        # f = QtCore.QFile(fileName)
        # if not f.open(QtCore.QFile.ReadOnly):
        #     return QtGui.QStringListModel(self.completer)

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        data = self.global_data

        QtGui.QApplication.restoreOverrideCursor()
        return QtGui.QStringListModel(data, self)
        #

    def build_completer(self):

        self.global_data.extend(web_api.dicts.keys())
        if self.run_data:
            self.global_data.extend(self.run_data)
        if self.local_data:
            self.global_data.extend(self.local_data)

        return self.global_data
