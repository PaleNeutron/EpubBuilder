__author__ = 'PaleNeutron'
import os
from urllib.parse import urlparse, unquote
import sys

from PySide import QtGui, QtCore


class MyMainWindow(QtGui.QMainWindow):
    file_loaded = QtCore.Signal(bool, str)

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.windowList = []
        self.text_path = ''
        self.epub_path = ''
        self.win_file_mime = "application/x-qt-windows-mime;value=\"FileNameW\""
        self.text_uri_mime = "text/uri-list"
        self.creat_content_broswer()

    def creat_content_broswer(self):
        self.content_browser = QtGui.QTextBrowser()
        self.content_browser.setGeometry(QtCore.QRect(300, 150, 600, 400))
        self.windowList.append(self.content_browser)

    def dragEnterEvent(self, ev):
        ev.accept()

    def load_file(self, file_path):
        self.file_loaded.emit(file_path)

    def image_loaded(self, file_path):
        with open(file_path, "b") as f:
            r = f.read()
        with open("images/cover.jpg", "wb") as f:
            f.write(r)

    # def epub_loaded(self, file_path):
    # self.epub_path = file_path
    # self.file_loaded.emit(False, )

    def uri_to_path(self, uri):
        if sys.platform == "win32":
            path = unquote(urlparse(uri).path)[1:]
        if sys.platform == "linux":
            path = unquote(urlparse(uri).path)

    def dropEvent(self, ev):
        # formats = ev.mimeData().formats()
        # for i in formats:
        # print(i)
        # if ev.mimeData().hasFormat(self.win_file_mime):
        # ev.accept()
        # file_path = bytes(ev.mimeData().data(self.win_file_mime).data())[:-2].decode('utf16')
        #     if file_path.endswith(".txt"):
        #         self.text_loaded(file_path)
        #     elif file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        #         self.image_loaded(file_path)
        #     elif file_path.endswith(".epub"):
        #         self.epub_loaded(file_path)
        #         print(file_path)
        if ev.mimeData().hasFormat(self.text_uri_mime):
            uri = str(ev.mimeData().data(self.text_uri_mime)).strip()
            if uri.endswith(".txt") or uri.endswith(".epub"):
                file_path = self.uri_to_path(uri)
                self.file_loaded(file_path)

            elif uri.endswith(".zip"):
                #打开一个zip文档，获取其中的txt
                zip_path = unquote(urlparse(uri).path)
                import zipfile

                zf = zipfile.ZipFile(zip_path)
                for fn in zf.namelist():
                    #如果文档中txt文件大于10kb则解压到当前文件夹
                    if fn.endswith(".txt") and zf.getinfo(fn).file_size > 10 * 1024:
                        zf.extract(fn)
                        #发送文件位置信号
                    self.text_loaded(os.curdir + os.sep + fn)
                    break
        else:
            ev.ignore()