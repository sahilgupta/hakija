#!/usr/bin/python

import re
import os
import sys
import urllib
import urllib2
import datetime
from zipfile import ZipFile
import requests


from PyQt4 import QtCore, QtGui
from gui import Ui_Hakija

from mechanize import Browser


class Hakija(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Hakija()
        self.ui.setupUi(self)

        self.ui.endDate.setDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.startDate.setDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.endDate.setMaximumDate(
            QtCore.QDateTime.currentDateTime().date())
        self.ui.startDate.setMaximumDate(
            QtCore.QDateTime.currentDateTime().date())

        # Disable cancel button
        self.ui.cancelButton.setDisabled(True)

        # Create thread object and connect its signals to methods on
        # this object
        self.ponderous = DownloadData()
        self.connect(self.ponderous,
                     QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                     self.appendUpdates)
        self.connect(self.ponderous,
                     QtCore.SIGNAL("finished()"),
                     self.downloadComplete)

        QtCore.QObject.connect(self.ui.downloadButton,
                               QtCore.SIGNAL("clicked()"),
                               self.startDownload)
        QtCore.QObject.connect(self.ui.cancelButton,
                               QtCore.SIGNAL("clicked()"),
                               self.cancelDownload)
        QtCore.QObject.connect(self.ui.actionExit,
                               QtCore.SIGNAL("triggered()"),
                               sys.exit)
        self.ui.actionExit.setShortcut("Ctrl+Q")

        QtCore.QObject.connect(self.ui.actionaboutHakija,
                               QtCore.SIGNAL("triggered()"),
                               self.aboutHakija)

    def aboutHakija(self):
        text = """
        <html>
            <head>
                <title></title>
            </head>
            <body>
                <p>
                    <span style="font-size: 22px;">
                        <strong>Hakija v1.0.1</strong>
                    </span>
                    <br />
                    Hakija lets you download End of Day data from NSE.
                </p>
                <p>Author : Sahil Gupta</p>
                <p>
                    <a href="http://www.github.com/sahilgupta/hakija"
                    target="_blank"> Hakija Source Code
                    <br />
                    </a>
                </p>
                <p>&nbsp;</p>
            </body>
        </html>
        """
        QtGui.QMessageBox.about(self, "About Hakija", text)

    # Method called asynchronously by other thread when progress should
    # be updated
    def appendUpdates(self, update):
        print update
        self.ui.progressUpdate.setText(self.ui.progressUpdate.text() +
                                       update + "\n")
        self.ui.scrollArea.verticalScrollBar().setValue(
            self.ui.scrollArea.verticalScrollBar().maximum())

    def startDownload(self):
        self.ui.downloadButton.setDisabled(True)
        self.ui.cancelButton.setEnabled(True)
        self.ui.startDate.setDisabled(True)
        self.ui.endDate.setDisabled(True)

        # Disable checkbox checkability once the download has started
        self.checkBoxDisability(True)

        startdate = str(self.ui.startDate.date().toString("dd-MM-yyyy"))
        enddate = str(self.ui.endDate.date().toString("dd-MM-yyyy"))
        self.ponderous.goNow(startdate,
                             enddate,
                             self.ui.bhavcopyCB.isChecked(),
                             self.ui.nseniftyCB.isChecked(),
                             self.ui.niftyjuniorCB.isChecked(),
                             self.ui.nse100CB.isChecked(),
                             self.ui.bankniftyCB.isChecked(),
                             self.ui.nsemidcapCB.isChecked(),
                             self.ui.nseitCB.isChecked(),
                             self.ui.nse500CB.isChecked(),
                             self.ui.midcap50CB.isChecked(),
                             self.ui.vixCB.isChecked())

    def cancelDownload(self):
        self.ponderous.stopTask()
        self.ui.downloadButton.setEnabled(True)
        self.ui.cancelButton.setDisabled(True)
        self.ui.startDate.setEnabled(True)
        self.ui.endDate.setEnabled(True)
        # Re-enable checkbox checkability once the download has been
        # cancelled
        self.checkBoxDisability(False)

    def checkBoxDisability(self, bool):
        self.ui.bhavcopyCB.setDisabled(bool)
        self.ui.nseniftyCB.setDisabled(bool)
        self.ui.niftyjuniorCB.setDisabled(bool)
        self.ui.nse100CB.setDisabled(bool)
        self.ui.bankniftyCB.setDisabled(bool)
        self.ui.nsemidcapCB.setDisabled(bool)
        self.ui.nseitCB.setDisabled(bool)
        self.ui.nse500CB.setDisabled(bool)
        self.ui.midcap50CB.setDisabled(bool)
        self.ui.vixCB.setDisabled(bool)

    def downloadComplete(self):
        self.ui.downloadButton.setEnabled(True)
        self.ui.cancelButton.setDisabled(True)
        self.ui.startDate.setEnabled(True)
        self.ui.endDate.setEnabled(True)
        # Re-enable checkbox checkability once the download is complete
        self.checkBoxDisability(False)


class DownloadData(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.data_dict = {}

    # Call this to launch the thread
    def goNow(self, startDate, endDate, bhavcopycb, nseniftycb, niftyjuniorcb,
              nse100cb, bankniftycb, nsemidcapcb, nseitcb, nse500cb,
              midcap50cb, vixcb):
        #def goNow(self, startDate, endDate, bhavcopycb):
        self.startdate = startDate
        self.enddate = endDate

        self.checklist = {'BHAVCOPY': bhavcopycb,
                          'NSENIFTY': nseniftycb,
                          'NIFTYJUNIOR': niftyjuniorcb,
                          'NSE100': nse100cb,
                          'NSE500': nse500cb,
                          'MIDCAP50': midcap50cb,
                          'NSEMIDCAP': nsemidcapcb,
                          'BANKNIFTY': bankniftycb,
                          'NSEIT': nseitcb,
                          'VIX': vixcb
                          }

        self.start()

    # This run method is called by Qt as a result of calling start()
    def run(self):
        self.stopping = False
        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                  "-------Starting the data download-------")
        self.stopping = False

        self.br = Browser()
        # Browser options
        self.br.set_handle_equiv(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        # Emulate a Mozilla Firefox 20.0 Browser to avoid the 403
        # Permission Denied Error
        self.host = 'www.nseindia.com'
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) \
                           Gecko/20100101 Firefox/20.0'
        self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.accept_language = 'en-US,en;q=0.5'
        self.accept_charset = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
        self.keep_alive = '115'
        self.connection = 'keep-alive'
        self.br.addheaders = [('Host', self.host),
                              ('User-Agent', self.user_agent),
                              ('Accept', self.accept),
                              ('Accept-Language', self.accept_language),
                              ('Accept-Charset', self.accept_charset),
                              ('Keep-Alive', self.keep_alive),
                              ('Connection', self.connection)]

        startdate = datetime.datetime.strptime(self.startdate,
                                               "%d-%m-%Y").date()
        enddate = datetime.datetime.strptime(self.enddate, "%d-%m-%Y").date()

        self.d = startdate
        delta = datetime.timedelta(days=1)
        while self.d <= enddate:
            flag = 0
            date = self.d.strftime("%d-%m-%Y")
            self.date = self.d.strftime("%d-%m-%Y")

            self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                      "-------" + date + "-------")

            try:
                self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                          "Log Message: Checking for data existence...")
                res = self.br.open("http://www.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date=" +
                                   date + "&section=EQ", timeout=10)

            except urllib2.URLError as e:
                if str(e) == "<urlopen error [Errno -2] Name or service not known>":
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                              "Log Message: No internet connection found. \
                              Kindly check and retry.")
                    self.stopTask()
            else:
                # Check if EOD data for the given date exists
                for link in self.br.links():
                    rlink = "http://nseindia.com" + link.url
                    # Flag to mark the existence of data.
                    flag = 1
                    break
                global curdir
                self.nfile = os.path.join(curdir,
                                          self.d.strftime("%d-%m-%Y") + ".txt")
                if self.checklist['BHAVCOPY']:
                    if flag:
                        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                                  "Log Message: Downloading bhavcopy...")

                        class AppURLopener(urllib.FancyURLopener):
                            version = self.user_agent

                        urllib._urlopener = AppURLopener()

                        urldata = urllib.urlretrieve(rlink,
                                                     None,
                                                     #reporthook
                                                     )

                        if self.stopping:
                            return
                        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                                  "Log Message: Bhavcopy succesfully fetched!")

                        file = ZipFile(urldata[0], "r")
                        data = file.read(file.namelist()[0])
                        file.close()
                        # delete the temp file created
                        urllib.urlcleanup()

                        x = data.split("\n")

                        for x1 in x[1:-1]:
                            x1 = x1.split(",")
                            # Extract and write only the EQ series
                            # data in the file
                            if x1[1] == "EQ":
                                try:
                                    self.data_dict[x1[0]] = x1[0] + "," + \
                                             self.d.strftime("%Y%m%d") + \
                                            "," + x1[2] + "," + x1[3] + \
                                            "," + x1[4] + "," + x1[5] + ","
                                except:
                                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                                              "Log Message: Error in \
                                              downloading Bhavcopy. \
                                              Kindly retry later.")

                        for row in self.get_delivery_data(self.d):
                          if row[1] == "EQ":
                            if self.data_dict.get(row[0]):
                              print row
                              self.data_dict[row[0]] += ','.join(row[2:])

                        with open(self.nfile, "w") as f:
                            for key in sorted(self.data_dict.iterkeys()):
                                f.write(self.data_dict[key] + "\r\n")
                            if self.downloadindexdata(f):
                                return
                    else:
                        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                                  "Log Message: No Data Found!.\n\n")
                elif flag:
                    with open(self.nfile, "a") as f:
                        if self.downloadindexdata(f):
                            # If the return was abnormal due to user
                            # cancellation. Stop the thread.
                            return
                else:
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                              "Log Message: No Data Found!.\n\n")

            self.d += delta
        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                  "--------Download Complete--------")
        self.emit(QtCore.SIGNAL("finished()"))

    def stopTask(self):
        self.stopping = True

    def get_delivery_data(self, date):
        req = requests.get('http://www.nseindia.com/archives/equities/mto/MTO_%s.DAT' % self.d.strftime("%d%m%Y"))
        return [z.strip().split(',')[2:] for z in req.content.split('\n')[4:-1]] # Remove the headers and the empty line at the end.

    def downloadindexdata(self, f):
        indexList = ['NSENIFTY',
                     'NIFTYJUNIOR',
                     'BANKNIFTY',
                     'NSEMIDCAP',
                     'NSEIT',
                     'NSE100',
                     'NSE500',
                     'MIDCAP50',
                     'VIX',
                     #'NSEDEFTY',
                     ]
        # Create a dictionary mapping index to the index data URL
        urls = {
        'NSENIFTY': 'http://nseindia.com/content/indices/histdata/CNX%20NIFTYdate-date.csv',
        'NIFTYJUNIOR': 'http://nseindia.com/content/indices/histdata/CNX%20NIFTY%20JUNIORdate-date.csv',
        'NSE100': 'http://nseindia.com/content/indices/histdata/CNX%20100date-date.csv',
        'NSE500': 'http://nseindia.com/content/indices/histdata/CNX%20500date-date.csv',
        'MIDCAP50': 'http://nseindia.com/content/indices/histdata/NIFTY%20MIDCAP%2050date-date.csv',
        'NSEMIDCAP': 'http://nseindia.com/content/indices/histdata/CNX%20MIDCAPdate-date.csv',
        'BANKNIFTY': 'http://nseindia.com/content/indices/histdata/BANK%20NIFTYdate-date.csv',
        'NSEIT': 'http://nseindia.com/content/indices/histdata/CNX%20ITdate-date.csv',
        'VIX': 'http://www.nseindia.com/content/vix/histdata/hist_india_vix_date_date.csv'
        }

        for index in indexList:
            # Check whether we've been cancelled or not
            if self.stopping:
                return 1
            if self.checklist[index]:
                newurl = re.sub('date', self.date, urls[index])
                self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                          "Log Message: Downloading " + index +
                          " index data...")
                try:
                    res = self.br.open(newurl, timeout=50)
                except:
                    print "EXCEPTION"
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                              "Log Message: Error in downloading " + index +
                              " index data. Kindly retry later.")
                else:
                    data = res.read().split("\n")[1]
                    abc = re.sub("\"", '', data).split(",")
                    a = []
                    for i in abc[1:]:
                        a.append(i.strip())
                    try:
                        f.write(index + "," + self.d.strftime("%Y%m%d") +
                                "," + a[0] + "," + a[1] + "," + a[2] + "," +
                                a[3] + "," + a[4] + "\r\n")
                    except IOError:
                        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                                  "Log Message: Error in downloading " +
                                  index + " index data. Kindly retry later.")
        f.close()
        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"),
                  "Log Message: File successfully written.\n\n")


thisdir = os.path.dirname(os.path.abspath(sys.argv[0]))
datadir = "EOD_Data"
curdir = os.path.join(thisdir, datadir)
if not os.path.isdir(curdir):
    os.mkdir(curdir)
    os.chdir(curdir)

# Start the program
app = QtGui.QApplication(sys.argv)
window = Hakija()
window.show()
sys.exit(app.exec_())
