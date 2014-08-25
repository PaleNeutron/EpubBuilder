__author__ = 'paleneutron'
from PySide import QtCore


class Messenger(QtCore.QObject):
    msg = QtCore.Signal(str)

    def __init__(self):
        super(Messenger, self).__init__()


process_rate = 0.0
m = Messenger()
message = m.msg