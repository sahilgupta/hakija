# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main-window-gui.ui'
#
# Created: Fri May 20 02:19:21 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Bhavcopy(object):
    def setupUi(self, Bhavcopy):
        Bhavcopy.setObjectName(_fromUtf8("Bhavcopy"))
        Bhavcopy.resize(473, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Bhavcopy.sizePolicy().hasHeightForWidth())
        Bhavcopy.setSizePolicy(sizePolicy)
        Bhavcopy.setAutoFillBackground(True)
        Bhavcopy.setAnimated(True)
        self.centralwidget = QtGui.QWidget(Bhavcopy)
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
        self.startDate = QtGui.QDateTimeEdit(self.centralwidget)
        self.startDate.setCalendarPopup(True)
        self.startDate.setObjectName(_fromUtf8("startDate"))
        self.horizontalLayout.addWidget(self.startDate)
        self.endDateLabel = QtGui.QLabel(self.centralwidget)
        self.endDateLabel.setObjectName(_fromUtf8("endDateLabel"))
        self.horizontalLayout.addWidget(self.endDateLabel)
        self.endDate = QtGui.QDateTimeEdit(self.centralwidget)
        self.endDate.setAccelerated(False)
        self.endDate.setCalendarPopup(True)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.horizontalLayout.addWidget(self.endDate)
        self.downloadButton = QtGui.QPushButton(self.centralwidget)
        self.downloadButton.setEnabled(True)
        self.downloadButton.setAutoDefault(True)
        self.downloadButton.setDefault(True)
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
        self.progressUpdate = QtGui.QLabel(self.centralwidget)
        self.progressUpdate.setAutoFillBackground(True)
        self.progressUpdate.setObjectName(_fromUtf8("progressUpdate"))
        self.verticalLayout_2.addWidget(self.progressUpdate)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        Bhavcopy.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Bhavcopy)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Bhavcopy.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(Bhavcopy)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 473, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        Bhavcopy.setMenuBar(self.menubar)

        self.retranslateUi(Bhavcopy)
        QtCore.QMetaObject.connectSlotsByName(Bhavcopy)

    def retranslateUi(self, Bhavcopy):
        Bhavcopy.setWindowTitle(QtGui.QApplication.translate("Bhavcopy", "NSE Data Downloader", None, QtGui.QApplication.UnicodeUTF8))
        self.startDateLabel.setText(QtGui.QApplication.translate("Bhavcopy", "  Start Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.startDate.setDisplayFormat(QtGui.QApplication.translate("Bhavcopy", "dd/MM/yy", None, QtGui.QApplication.UnicodeUTF8))
        self.endDateLabel.setText(QtGui.QApplication.translate("Bhavcopy", "    End Date:", None, QtGui.QApplication.UnicodeUTF8))
        self.endDate.setDisplayFormat(QtGui.QApplication.translate("Bhavcopy", "dd/MM/yy", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("Bhavcopy", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.downlaodedLabel.setText(QtGui.QApplication.translate("Bhavcopy", "Downloaded:", None, QtGui.QApplication.UnicodeUTF8))
        self.progressUpdate.setText(QtGui.QApplication.translate("Bhavcopy", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Bhavcopy = QtGui.QMainWindow()
    ui = Ui_Bhavcopy()
    ui.setupUi(Bhavcopy)
    Bhavcopy.show()
    sys.exit(app.exec_())

