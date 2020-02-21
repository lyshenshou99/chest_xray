# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QApplication)
from PyQt5.QtGui import QPixmap
from solve import Solve


class Ui_mainWindow(QtWidgets.QMainWindow):

    path = ''

    def __init__(self):
        super(Ui_mainWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.radioButton_image = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_image.setGeometry(QtCore.QRect(560, 40, 131, 41))
        self.radioButton_image.setObjectName("radioButton_image")

        self.radioButton_folder = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_folder.setGeometry(QtCore.QRect(560, 80, 131, 51))
        self.radioButton_folder.setObjectName("radioButton_folder")

        self.listView_picture = QtWidgets.QListView(self.centralwidget)
        self.listView_picture.setGeometry(QtCore.QRect(40, 30, 500, 300))
        self.listView_picture.setObjectName("listView_picture")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(580, 440, 171, 111))
        self.pushButton.setObjectName("pushButton")

        self.listEdit_result = QtWidgets.QLineEdit(self.centralwidget)
        self.listEdit_result.setGeometry(QtCore.QRect(570, 300, 200, 30))
        self.listEdit_result.setObjectName("listView_result")

        self.lineEdit_path = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_path.setGeometry(QtCore.QRect(110, 410, 361, 31))
        self.lineEdit_path.setObjectName("lineEdit_path")

        self.pushButton_choosepath = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_choosepath.setGeometry(QtCore.QRect(170, 490, 241, 31))
        self.pushButton_choosepath.setObjectName("pushButton_choosepath")

        self.label_picture = QtWidgets.QLabel(self.centralwidget)
        self.label_picture.setGeometry(QtCore.QRect(40, 30, 501, 301))
        self.label_picture.setObjectName("label_picture")

        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

        self.pushButton_choosepath.clicked.connect(self.openfile)
        self.pushButton.clicked.connect(self.Predection)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "康康肺吧--你的肺部健康管家"))
        self.radioButton_image.setText(_translate("mainWindow", "Image"))
        self.radioButton_folder.setText(_translate("mainWindow", "Folder"))
        self.pushButton.setText(_translate("mainWindow", "Predection"))
        self.lineEdit_path.setText(_translate("mainWindow", "path"))
        self.pushButton_choosepath.setText(_translate("mainWindow", "Click here to choose the path"))

    def openfile(self):
        if self.radioButton_image.isChecked():
            path = QFileDialog.getOpenFileName(self, '选择文件', './')
            self.lineEdit_path.setText(str(path[0]))
            result = str(path[0])
            self.label_picture.setPixmap(QPixmap(result))
            self.label_picture.setScaledContents(True)

        if self.radioButton_folder.isChecked():
            path = QFileDialog.getExistingDirectory(self, '选择文件夹', './')
            self.lineEdit_path.setText(str(path))
            result = r'folder.jpg'
            self.label_picture.setPixmap(QPixmap(result))

    def Predection(self):
        MODEL_PATH = r'weights.06.hdf5'
        if self.radioButton_image.isChecked():
            images0 = self.lineEdit_path.displayText()
            s = Solve(MODEL_PATH, image=images0)
            result = str(s.solve_one())
            self.listEdit_result.setText(result)

        if self.radioButton_folder.isChecked():
            folder0 = self.lineEdit_path.displayText()
            s = Solve(path=MODEL_PATH, folder=folder0)
            s.solve_excel()
            result = 'Picture_set.xls'
            self.listEdit_result.setText(result)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())