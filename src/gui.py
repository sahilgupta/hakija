# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main-window-gui.ui'
#
# Created: Thu May 19 16:11:47 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(473, 300)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startDateLabel = QtGui.QLabel(self.centralwidget)
        self.startDateLabel.setObjectName(_fromUtf8("startDateLabel"))
        self.horizontalLayout.addWidget(self.startDateLabel)
        self.startDate = QtGui.QDateEdit(self.centralwidget)
        self.startDate.setObjectName(_fromUtf8("startDate"))
        self.horizontalLayout.addWidget(self.startDate)
        self.endDateLabel = QtGui.QLabel(self.centralwidget)
        self.endDateLabel.setObjectName(_fromUtf8("endDateLabel"))
        self.horizontalLayout.addWidget(self.endDateLabel)
        self.endDate = QtGui.QDateEdit(self.centralwidget)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.horizontalLayout.addWidget(self.endDate)
        self.downloadButton = QtGui.QPushButton(self.centralwidget)
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.horizontalLayout.addWidget(self.downloadButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.downlaodedLabel = QtGui.QLabel(self.centralwidget)
        self.downlaodedLabel.setObjectName(_fromUtf8("downlaodedLabel"))
        self.horizontalLayout_2.addWidget(self.downlaodedLabel)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty(_fromUtf8("value"), 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 473, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.startDate, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), MainWindow.setStartDate)
        QtCore.QObject.connect(self.startDate, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.setStartDate)
        QtCore.QObject.connect(self.endDate, QtCore.SIGNAL(_fromUtf8("dateChanged(QDate)")), MainWindow.setEndDate)
        QtCore.QObject.connect(self.endDate, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.setEndDate)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.startDownload)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.lower)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.checkDateVaildity)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.startDateLabel.setText(QtGui.QApplication.translate("MainWindow", "Start Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.endDateLabel.setText(QtGui.QApplication.translate("MainWindow", "End Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("MainWindow", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.downlaodedLabel.setText(QtGui.QApplication.translate("MainWindow", "Downloaded:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

