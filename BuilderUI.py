#!/opt/python3.4.1/bin/python3
import urllib.parse
import os
import subprocess

import TinyEpub
from PySide import QtCore, QtGui

import ui_mainwindow
import my_mainwindow
import web_info
import neattxt
import txt2html
import arrange
import strucreat
import epubzip
import messager


class BuilderUI(ui_mainwindow.Ui_MainWindow):
    """the mainUI for EpubBuilder, contains the signal and slot"""

    def __init__(self):
        super(BuilderUI, self).__init__()
        if sys.platform == "win32":
            self.editor_path = "notepad"
        elif sys.platform == "linux":
            self.editor_path = "gvim"
            # self.editor_path = "subl"

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
        self.txt_folder = os.path.expanduser('~/Documents/txt')
        self.epub_folder = os.path.expanduser('~/Documents/epub')
        self.image_folder = "./images"
        self.ensure_directory(self.txt_folder, self.epub_folder, self.image_folder)
        self.book_info = web_info.WebInfo()
        self.message = messager.message
        self.main_window = my_mainwindow.MyMainWindow()
        self.setupUi(self.main_window)

        self.pushButton_get_info.clicked.connect(self.get_info)
        self.lineEdit_title.textChanged.connect(self.to_bookpage)
        self.pushButton_start_build.clicked.connect(self.build)
        self.pushButton_edit_text.clicked.connect(self.edit_text)
        self.main_window.file_loaded.connect(self.load_file)
        self.radioButton_qidian.clicked.connect(self.choose_site)
        self.radioButton_chuangshi.clicked.connect(self.choose_site)
        self.radioButton_zongheng.clicked.connect(self.choose_site)
        self.message.connect(self.statusbar.showMessage)
        self.progressBar.setValue(messager.process_rate)

    def ensure_directory(self, *dir_list):
        for d in dir_list:
            if not os.path.isdir(d):
                os.makedirs(d)

    # #self.label_cover.setPixmap(QtGui.QPixmap(os.getcwd() + '/images/cover.jpg'))

    @QtCore.Slot(str)
    def load_file(self, file_path):
        if file_path.endswith(".txt"):
            self.title = os.path.basename(os.path.splitext(file_path)[0])
            self.load_text()
        else:
            self.load_epub()
        self.lineEdit_title.setText(self.title)
        self.check_has_txt()

    @QtCore.Slot(str)
    def to_bookpage(self, title):
        p = True
        for c in title:
            p = p and (c in "1234567890")
        if p and len(title) < 8:
            url = "http://www.qidian.com/Book/%s.aspx" % title
        elif p and len(title) >= 8:
            url = "http://chuangshi.qq.com/bk/ls/%s-1.html" % title
        # if p:
        # self.bookid=p
        else:
            url = 'http://www.lkong.net/book.php?mod=view&bookname=' + urllib.parse.quote(title)
        self.lineEdit_bookpage.setText(url)

    def choose_site(self):
        sender = self.main_window.sender()
        self.statusbar.showMessage(repr(sender))

    def edit_text(self):
        subprocess.Popen([self.editor_path, self.file_path])

    def load_text(self):
        self.file_path = self.main_window.text_path
        self.pushButton_start_build.setEnabled(True)
        self.pushButton_edit_text.setEnabled(True)

    def load_epub(self):
        book = TinyEpub.Epub(self.main_window.epub_path)
        self.title = book.title
        self.author = book.author
        self.description = book.description
        self.chr_pattern = book.chrpattern
        self.cover_byte = book.cover
        line = self.comboBox_re.lineEdit()
        line.setText(self.chr_pattern)
        self.lineEdit_title.setText(self.title)
        self.lineEdit_author.setText(self.author)
        self.textEdit_chapter.setDocument(QtGui.QTextDocument(self.description))
        self.cover.loadFromData(QtCore.QByteArray(self.cover_byte))
        self.label_cover.clear()
        self.label_cover.setPixmap(self.cover)

    def get_info(self):
        self.book_info.url = self.lineEdit_bookpage.text()
        self.book_info.open_page()
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
        if self.title + ".txt" in os.listdir(self.txt_folder):
            self.file_path = self.txt_folder + os.sep + self.title + ".txt"
            if not self.pushButton_start_build.isEnabled():
                self.pushButton_start_build.setEnabled(True)
                self.pushButton_edit_text.setEnabled(True)

    def build(self):
        self.title = self.lineEdit_title.text()
        self.author = self.lineEdit_author.text()
        self.chr_pattern = self.comboBox_re.currentText()
        self.description = self.textEdit_chapter.document().toPlainText()
        if not self.cover.isNull():
            self.cover.save(os.getcwd() + '/images/cover.jpg')
        self.label_cover.setPixmap(QtGui.QPixmap(os.getcwd() + '/images/cover.jpg'))

        text = neattxt.get_neat_txt(self.file_path, self.title, self.txt_folder).split("\n")
        txt2html.format_txt(self.title, self.author, text, self.description, self.chr_pattern)
        self.message.emit('arrange is done')
        strucreat.structure(self.description, self.chr_pattern)
        self.message.emit('structure is done')
        epubzip.epubzip('epubobject', self.title)
        arrange.arrange(self.file_path, self.txt_folder, self.epub_folder, self.title)
        self.message.emit('arrange is done')
        self.file_path = self.txt_folder + os.sep + self.title + '.txt'

        self.show_contents()

    def show_contents(self):
        with open('contents.txt', encoding='utf8') as f:
            r = f.read()
        # self.main_window.content_browser.clear()
        self.main_window.content_browser.setText(r)
        self.main_window.content_browser.show()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    ui = BuilderUI()
    ui.main_window.show()
    sys.exit(app.exec_())
