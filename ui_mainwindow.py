# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/paleneutron/Database/EpubBuilder/ui_mainwindow.ui'
#
# Created: Mon Aug 25 11:14:34 2014
# by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 421)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_edit_text = QtGui.QPushButton(self.centralwidget)
        self.pushButton_edit_text.setEnabled(False)
        self.pushButton_edit_text.setObjectName("pushButton_edit_text")
        self.horizontalLayout.addWidget(self.pushButton_edit_text)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.pushButton_start_build = QtGui.QPushButton(self.centralwidget)
        self.pushButton_start_build.setEnabled(False)
        self.pushButton_start_build.setObjectName("pushButton_start_build")
        self.horizontalLayout.addWidget(self.pushButton_start_build)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_bookpage = QtGui.QLabel(self.centralwidget)
        self.label_bookpage.setObjectName("label_bookpage")
        self.horizontalLayout_3.addWidget(self.label_bookpage)
        self.lineEdit_bookpage = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_bookpage.setObjectName("lineEdit_bookpage")
        self.horizontalLayout_3.addWidget(self.lineEdit_bookpage)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.radioButton_qidian = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_qidian.setChecked(True)
        self.radioButton_qidian.setObjectName("radioButton_qidian")
        self.horizontalLayout_8.addWidget(self.radioButton_qidian)
        self.radioButton_chuangshi = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_chuangshi.setObjectName("radioButton_chuangshi")
        self.horizontalLayout_8.addWidget(self.radioButton_chuangshi)
        self.radioButton_zongheng = QtGui.QRadioButton(self.centralwidget)
        self.radioButton_zongheng.setObjectName("radioButton_zongheng")
        self.horizontalLayout_8.addWidget(self.radioButton_zongheng)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_re = QtGui.QLabel(self.centralwidget)
        self.label_re.setTextFormat(QtCore.Qt.AutoText)
        self.label_re.setObjectName("label_re")
        self.horizontalLayout_2.addWidget(self.label_re)
        self.comboBox_re = QtGui.QComboBox(self.centralwidget)
        self.comboBox_re.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_re.setEditable(True)
        self.comboBox_re.setObjectName("comboBox_re")
        self.comboBox_re.addItem("")
        self.comboBox_re.addItem("")
        self.comboBox_re.addItem("")
        self.comboBox_re.addItem("")
        self.comboBox_re.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_re)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textEdit_chapter = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_chapter.setObjectName("textEdit_chapter")
        self.verticalLayout.addWidget(self.textEdit_chapter)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_cover = QtGui.QLabel(self.centralwidget)
        self.label_cover.setMaximumSize(QtCore.QSize(210, 280))
        self.label_cover.setScaledContents(True)
        self.label_cover.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cover.setObjectName("label_cover")
        self.verticalLayout_2.addWidget(self.label_cover)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_title = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_6.addWidget(self.label_title)
        self.lineEdit_title = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_title.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_title.setObjectName("lineEdit_title")
        self.horizontalLayout_6.addWidget(self.lineEdit_title)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_author = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_author.setFont(font)
        self.label_author.setObjectName("label_author")
        self.horizontalLayout_5.addWidget(self.label_author)
        self.lineEdit_author = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_author.setObjectName("lineEdit_author")
        self.horizontalLayout_5.addWidget(self.lineEdit_author)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pushButton_get_info = QtGui.QPushButton(self.centralwidget)
        self.pushButton_get_info.setObjectName("pushButton_get_info")
        self.horizontalLayout_4.addWidget(self.pushButton_get_info)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.setStretch(0, 4)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 28))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.label_bookpage.setBuddy(self.lineEdit_bookpage)
        self.label_re.setBuddy(self.comboBox_re)
        self.label_title.setBuddy(self.lineEdit_title)
        self.label_author.setBuddy(self.lineEdit_author)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "EpubBuilder", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_edit_text.setText(
            QtGui.QApplication.translate("MainWindow", "编辑文本", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_start_build.setText(
            QtGui.QApplication.translate("MainWindow", "开始", None, QtGui.QApplication.UnicodeUTF8))
        self.label_bookpage.setText(
            QtGui.QApplication.translate("MainWindow", "书页网址", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_qidian.setText(
            QtGui.QApplication.translate("MainWindow", "起点", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_chuangshi.setText(
            QtGui.QApplication.translate("MainWindow", "创世", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_zongheng.setText(
            QtGui.QApplication.translate("MainWindow", "纵横", None, QtGui.QApplication.UnicodeUTF8))
        self.label_re.setText(
            QtGui.QApplication.translate("MainWindow", "章节划分正则表达式", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_re.setItemText(0, QtGui.QApplication.translate("MainWindow",
                                                                     "^(序|第[\\d零〇一二两三四五六七八九十百千]{0,10})章.{0,20}$", None,
                                                                     QtGui.QApplication.UnicodeUTF8))
        self.comboBox_re.setItemText(1, QtGui.QApplication.translate("MainWindow",
                                                                     "^第[\\d零〇一二两三四五六七八九十百千]{0,10}卷.{0,20}(序|第[\\d零〇一二三四五六七八九十百千]{0,10})章.{0,20}$",
                                                                     None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_re.setItemText(2, QtGui.QApplication.translate("MainWindow",
                                                                     "^.{0,5}第[\\d零〇一二两三四五六七八九十百千]{0,10}章.{0,20}$",
                                                                     None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_re.setItemText(3, QtGui.QApplication.translate("MainWindow", "^\\d{1,4}.{1,30}$", None,
                                                                     QtGui.QApplication.UnicodeUTF8))
        self.comboBox_re.setItemText(4, QtGui.QApplication.translate("MainWindow",
                                                                     "^[\\d零〇一二两三四五六七八九十百千]{1,10}[、 ]{1,3}.{0,20}$",
                                                                     None, QtGui.QApplication.UnicodeUTF8))
        self.label_cover.setText(QtGui.QApplication.translate("MainWindow", "封面", None, QtGui.QApplication.UnicodeUTF8))
        self.label_title.setText(
            QtGui.QApplication.translate("MainWindow", "书名：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_author.setText(
            QtGui.QApplication.translate("MainWindow", "作者：", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_get_info.setText(
            QtGui.QApplication.translate("MainWindow", "抓取信息", None, QtGui.QApplication.UnicodeUTF8))

