__author__ = 'paleneutron'
from PyQt5 import QtCore


class Messenger(QtCore.QObject):
    msg = QtCore.pyqtSignal(str)
    update_rate = QtCore.pyqtSignal(float)
    page_opened = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()
    text_neated = QtCore.pyqtSignal()

    def __init__(self):
        super(Messenger, self).__init__()


__messager__ = Messenger()
statusbar_message = __messager__.msg
process_message = __messager__.update_rate
process_rate_list = [0, 0, 0, 70, 85, 90, 95]

page_opened = __messager__.page_opened
finished = __messager__.finished
text_neated = __messager__.text_neated

def get_rate(rate_status, ratio):
    return process_rate_list[rate_status - 1] + (process_rate_list[rate_status] - process_rate_list[
        rate_status - 1]) * ratio