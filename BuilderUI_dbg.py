import urllib.parse
import os
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import TinyEpub
import ui_mainwindow
import my_mainwindow
import web_info
import neattxt
import txt2html
import arrange
import strucreat
import epubzip
import messager


class BuilderUI_dbg(ui_mainwindow.Ui_MainWindow):
    """the mainUI for EpubBuilder, contains the signal and.pyqtSlot"""

    def __init__(self):
        super(BuilderUI_dbg, self).__init__()
        # set open method depends on platform
        if sys.platform == "win32":
            self.system_open = os.startfile
            from win32com.shell import shell, shellcon
            mydocument_path = shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0)
            self.txt_folder = mydocument_path + os.sep + 'txt'
            self.epub_folder = mydocument_path + os.sep + 'epub'
        elif sys.platform == "linux":
            self.system_open = lambda path: subprocess.Popen(["xdg-open",path])
            self.txt_folder = os.path.expanduser('~/Documents/txt')
            self.epub_folder = os.path.expanduser('~/Documents/epub')

        self.file_path = ''
        self.bookid = ''
        self.title = ''
        self.author = ''
        self.web_address = ''
        self.chr_pattern = ''
        self.description = ''
        self.cover_byte = b''
        self.cover = QtGui.QPixmap()
        self.mine_type = 'application/x-qt-windows-mime;value=\"FileNameW\"'
        self.image_folder = "./images"
        self.ensure_directory(self.txt_folder, self.epub_folder)
        self.book_info = web_info.BookInfo()
        self.message = messager.statusbar_message
        self.rate = messager.process_message
        self.main_window = my_mainwindow.MyMainWindow()
        self.setupUi(self.main_window)

        self.pushButton_get_info.clicked.connect(self.open_url)
        self.lineEdit_title.textChanged.connect(self.to_bookpage)
        self.pushButton_start_build.clicked.connect(self.build)
        self.pushButton_edit_text.clicked.connect(self.edit_text)
        self.main_window.file_loaded.connect(self.load_file)
        self.main_window.image_loaded.connect(self.load_image)
        self.radioButton_qidian.clicked.connect(self.choose_site)
        self.radioButton_chuangshi.clicked.connect(self.choose_site)
        self.radioButton_zongheng.clicked.connect(self.choose_site)
        self.message.connect(self.statusbar.showMessage)
        self.rate.connect(self.progressBar.setValue)
        messager.page_opened.connect(self.get_info)
        messager.finished.connect(self.finish_build)
        messager.text_neated.connect(self.reset_progressbar)

    def ensure_directory(self, *dir_list):
        for d in dir_list:
            if not os.path.isdir(d):
                os.makedirs(d)

    @QtCore.pyqtSlot(str)
    def load_file(self, file_path):
        if file_path.endswith(".txt"):
            self.file_path = file_path
            self.title = os.path.basename(os.path.splitext(file_path)[0])
            self.load_text()
        else:
            self.load_epub(file_path)
            self.check_has_txt()
        self.lineEdit_title.setText(self.title)

    @QtCore.pyqtSlot(str)
    def to_bookpage(self, title):
        p = True
        for c in title:
            p = p and (c in "1234567890")
        if p:
            self.bookid = title
            if len(self.bookid) < 8:  # 目前的判断规则没法直接从文件名区别是起点还是纵横，甚至有时候几乎不能自行分清起点和创世
                url = "http://www.qidian.com/Book/%s.aspx" % self.bookid
            else:
                url = "http://chuangshi.qq.com/bk/ls/%s.html" % self.bookid  # 警告！网址中的ls是"历史"的含义，虽不影响使用，但是十分危险
        else:
            url = 'http://www.lkong.net/book.php?mod=view&bookname=' + urllib.parse.quote(title)
        self.lineEdit_bookpage.setText(url)

    @QtCore.pyqtSlot(QtGui.QImage)
    def load_image(self, cover_image):
        self.cover_byte = cover_image
        self.cover.convertFromImage(cover_image)
        self.label_cover.clear()
        self.label_cover.setPixmap(self.cover)

    def choose_site(self):
        sender = self.main_window.sender()
        url = ''
        if sender is self.radioButton_chuangshi:
            url = "http://chuangshi.qq.com/bk/ls/%s.html" % self.bookid
        elif sender is self.radioButton_qidian:
            url = "http://www.qidian.com/Book/%s.aspx" % self.bookid
        elif sender is self.radioButton_zongheng:
            url = "http://book.zongheng.com/book/%s.html" % self.bookid
        self.lineEdit_bookpage.setText(url)

    def edit_text(self):
        self.system_open(self.file_path)

    def load_text(self):
        self.pushButton_start_build.setEnabled(True)
        self.pushButton_edit_text.setEnabled(True)

    def load_epub(self, file_path):
        book = TinyEpub.Epub(file_path)
        self.title = book.title
        self.author = book.author
        self.description = book.description
        self.chr_pattern = book.chrpattern
        self.cover_byte = book.cover
        self.comboBox_re.lineEdit().setText(self.chr_pattern)
        self.lineEdit_title.setText(self.title)
        self.lineEdit_author.setText(self.author)
        self.textEdit_chapter.setDocument(QtGui.QTextDocument(self.description))
        self.cover.loadFromData(QtCore.QByteArray(self.cover_byte))
        self.label_cover.clear()
        self.label_cover.setPixmap(self.cover)

    def open_url(self):
        self.book_info.url = self.lineEdit_bookpage.text()
        self.book_info.open_page()

    def get_info(self):
        if self.book_info.title:
            self.title = self.book_info.title
            self.author = self.book_info.author
            self.description = self.book_info.description
            self.lineEdit_bookpage.setText(self.book_info.url)
            self.lineEdit_title.setText(self.title)
            self.lineEdit_author.setText(self.author)
            self.textEdit_chapter.setDocument(QtGui.QTextDocument(self.description))
            self.cover_byte = self.book_info.cover
            self.cover.loadFromData(QtCore.QByteArray(self.cover_byte))
            self.label_cover.clear()
            self.label_cover.setPixmap(self.cover)
            self.check_has_txt()

    def check_has_txt(self):
        if self.title + ".txt" in os.listdir(self.txt_folder) and self.txt_folder in self.file_path:
            self.file_path = self.txt_folder + os.sep + self.title + ".txt"
            if not self.pushButton_start_build.isEnabled():
                self.pushButton_start_build.setEnabled(True)
                self.pushButton_edit_text.setEnabled(True)

    def pre_build(self):
        self.title = self.lineEdit_title.text()
        self.author = self.lineEdit_author.text()
        self.chr_pattern = self.comboBox_re.currentText()
        self.description = self.textEdit_chapter.document().toPlainText()
        if 'images' not in os.listdir('.'):
            os.mkdir('images')
        if not self.cover.isNull():
            self.cover.save(os.getcwd() + '/images/cover.jpg')
        self.label_cover.setPixmap(QtGui.QPixmap(os.getcwd() + '/images/cover.jpg'))
        self.progressBar.setMaximum(0)
        self.progressBar.setMinimum(0)

    def generate_epub(self):
        text = neattxt.get_neat_txt(self.file_path, self.title, self.txt_folder).split("\n")
        messager.text_neated.emit()
        txt2html.format_txt(self.title, self.author, text, self.description, self.txt_folder, self.chr_pattern)
        self.message.emit('split is done')
        strucreat.structure(self.description, self.chr_pattern)
        self.message.emit('structure is done')
        epubzip.epubzip('epubobject', self.title)
        arrange.arrange(self.file_path, self.txt_folder, self.epub_folder, self.title)
        messager.process_message.emit(100)
        self.message.emit('arrange is done')
        messager.finished.emit()

    def build(self):
        self.pre_build()
        self.generate_epub()

    def finish_build(self):
        self.file_path = self.txt_folder + os.sep + self.title + '.txt'
        self.show_contents()

    def show_contents(self):
        with open('contents.txt', encoding='utf8') as f:
            r = f.read()
        # self.main_window.content_browser.clear()
        self.main_window.content_browser.setText(r)
        self.main_window.content_browser.show()

    def reset_progressbar(self):
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)

if __name__ == '__main__':
    # fix a bug in pyqt5
    # if sys.platform == "win32":
    # os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.dirname(QtCore.__file__) + "/plugins/platforms"
    # it doesn't work on another machine without pyqt installed. Copy libEGL.dll to the work dir will fix it.
    # err_log = open("error.log", "a")
    # sys.stderr = err_log #redirct STDERR
    app = QtWidgets.QApplication(sys.argv)
    ui = BuilderUI_dbg()
    ui.main_window.show()
    sys.exit(app.exec_())
