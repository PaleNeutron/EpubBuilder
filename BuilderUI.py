#!/usr/bin/python
import sys

from PyQt5 import QtCore, QtWidgets

import BuilderUI_dbg

class BuilderUI(BuilderUI_dbg.BuilderUI_dbg):
    """Multi-thread version main UI"""
    def __init__(self):
        super(BuilderUI, self).__init__()
        self.open_url_thread = WorkThread(self.open_url)
        self.build_thread = WorkThread(self.generate_epub)
        self.pushButton_get_info.clicked.connect(self.open_url_thread.start)

    def build(self):
        self.pre_build()
        self.build_thread.start()

class WorkThread(QtCore.QThread):
    def __init__(self, function):
        super(WorkThread, self).__init__()
        self.function = function

    def run(self):
        self.function()


if __name__ == '__main__':
    # fix a bug in pyqt5
    # if sys.platform == "win32":
    # os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.dirname(QtCore.__file__) + "/plugins/platforms"
    # it doesn't work on another machine without pyqt installed. Copy libEGL.dll to the work dir will fix it.
    # err_log = open("error.log", "a")  #redirct STDERR
    # sys.stderr = err_log
    app = QtWidgets.QApplication(sys.argv)
    ui = BuilderUI()
    ui.main_window.show()
    sys.exit(app.exec_())
