__author__ = 'PaleNeutron'
import os
from urllib.parse import urlparse, unquote
import sys

from PyQt5 import QtWidgets, QtCore, QtGui


class MyMainWindow(QtWidgets.QMainWindow):
    file_loaded = QtCore.pyqtSignal(str)
    image_loaded = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.windowList = []
        self.text_path = ''
        self.epub_path = ''
        self.win_file_mime = "application/x-qt-windows-mime;value=\"FileNameW\""
        self.text_uri_mime = "text/uri-list"
        self.create_content_browser()

    def create_content_browser(self):
        self.content_browser = QtWidgets.QTextBrowser()
        self.content_browser.setGeometry(QtCore.QRect(300, 150, 600, 400))
        self.windowList.append(self.content_browser)

    def dragEnterEvent(self, ev):
        ev.accept()

    def load_file(self, file_path):
        self.file_loaded.emit(file_path)

    # def image_loaded(self, file_path):
    #     with open(file_path, "b") as f:
    #         r = f.read()
    #     with open("images/cover.jpg", "wb") as f:
    #         f.write(r)

    # def epub_loaded(self, file_path):
    # self.epub_path = file_path
    # self.file_loaded.emit(False, )

    def uri_to_path(self, uri):
        if sys.platform == "win32":
            path = unquote(urlparse(uri).path)[1:]
        elif sys.platform == "linux":
            path = unquote(urlparse(uri).path)
        else:
            path = None
        return path

    def dropEvent(self, ev):
        # formats = ev.mimeData().formats()
        # for i in formats:
        # print(i)
        # if ev.mimeData().hasFormat(self.win_file_mime):
        # ev.accept()
        # file_path = bytes(ev.mimeData().data(self.win_file_mime).data())[:-2].decode('utf16')
        # if file_path.endswith(".txt"):
        #         self.text_loaded(file_path)
        #     elif file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        #         self.image_loaded(file_path)
        #     elif file_path.endswith(".epub"):
        #         self.epub_loaded(file_path)
        #         print(file_path)
        if ev.mimeData().hasImage():
            self.image_loaded.emit(ev.mimeData().imageData())
        if ev.mimeData().hasFormat(self.text_uri_mime):
            uri = ev.mimeData().data(self.text_uri_mime).data().decode("utf8").strip()
            file_path = self.uri_to_path(uri)

            if uri.lower().endswith(".txt") or uri.lower().endswith(".epub"):
                self.load_file(file_path)

            elif uri.lower().endswith(".zip"):
                #打开一个zip文档，获取其中的txt
                import zipfile

                zf = zipfile.ZipFile(file_path)
                for filename in zf.namelist():
                    #如果文档中txt文件大于10kb则解压到当前文件夹
                    if filename.lower().endswith(".txt") and zf.getinfo(filename).file_size > 10 * 1024:
                        zf.extract(filename)
                        # 发送文件位置信号
                    self.load_file(os.curdir + os.sep + filename)
                    break
            elif uri.lower().endswith(".rar"):
                import rarfile

                rf = rarfile.RarFile(file_path)
                for filename in rf.namelist():
                    # 如果文档中txt文件大于10kb则解压到当前文件夹
                    if filename.lower().endswith(".txt") and rf.getinfo(filename).file_size > 10 * 1024:
                        rf.extract(filename)
                        #发送文件位置信号
                    self.load_file(os.curdir + os.sep + filename)
                    break
        else:
            ev.ignore()