__author__ = 'PaleNeutron'
import os
from urllib.parse import urlparse, unquote

from PySide import QtGui, QtCore


class MyMainWindow(QtGui.QMainWindow):
    file_loaded = QtCore.Signal(bool, str)

    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.text_path = ''
        self.epub_path = ''
        self.win_file_mime = "application/x-qt-windows-mime;value=\"FileNameW\""
        self.text_url_mime = "text/uri-list"

    def dragEnterEvent(self, ev):
        ev.accept()
        # formats = ev.mimeData().formats()
        # for i in formats:
        # print(i)
        # if True:
        # if ev.mimeData().hasFormat(self.mine_type):
        #     ev.accept()
        # else:
        #     ev.ignore()
        # formats = ev.mimeData().formats()
        # for i in formats:
        #     # print(i)
        #     if i=="text/uri-list":
        #         print(i,"   ",repr(ev.mimeData().data(i)))

        # #            print(i,"   ",ev.mimeData().data(i))

    # #        with open("formats.txt", "ab") as f:
    ##            for i in formats:
    ##                f.write(("\n"+i+"\n").encode("UTF16"))
    ##                f.write(ev.mimeData().data(i))
    def text_loaded(self, file_path):
        self.text_path = file_path
        self.file_loaded.emit(True, os.path.basename(os.path.splitext(file_path)[0]))

    def image_loaded(self, file_path):
        with open(file_path, "b") as f:
            r = f.read()
        with open("images/cover.jpg", "wb") as f:
            f.write(r)

    def epub_loaded(self, file_path):
        self.epub_path = file_path
        self.file_loaded.emit(False, os.path.basename(os.path.splitext(file_path)[0]))

    def dropEvent(self, ev):
        formats = ev.mimeData().formats()
        for i in formats:
            print(i)
        if ev.mimeData().hasFormat(self.win_file_mime):
            ev.accept()
            file_path = bytes(ev.mimeData().data(self.win_file_mime).data())[:-2].decode('utf16')
            if file_path.endswith(".txt"):
                self.text_loaded(file_path)
            elif file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
                self.image_loaded(file_path)
            elif file_path.endswith(".epub"):
                self.epub_loaded(file_path)
        elif ev.mimeData().hasFormat(self.text_url_mime):
            url = str(ev.mimeData().data(self.text_url_mime)).strip()
            if url.endswith(".txt"):
                file_path = unquote(urlparse(url).path)
                # file_path = file_path[1:]
                print(file_path)
                self.text_loaded(file_path)
            elif url.endswith(".zip"):
                #打开一个zip文档，获取其中的txt
                zip_path = unquote(urlparse(url).path)
                import zipfile
                zf = zipfile.ZipFile(zip_path)
                for fn in zf.namelist():
                    #如果文档中txt文件大于10kb则解压到当前文件夹
                    if fn.endswith(".txt") and zf.getinfo(fn).file_size>10*1024:
                        zf.extract(fn)
                        #发送文件位置信号
                    self.text_loaded(os.curdir+os.sep+fn)
                    break
                # to be continue
        else:
            ev.ignore()