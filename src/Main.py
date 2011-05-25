#TODO: Handle incomplete file downloads due to net disconnection.
#TODO: Handle incomplete file written on the disk due to abrupt program exit.
#TODO: Handle no internet connection with a timeout
#TODO: Individual Time out for different Index data downloads

from PyQt4 import QtCore, QtGui
from gui import  Ui_Bhavcopy
import time, re,socket
import sys, urllib, datetime
from mechanize import Browser
from zipfile import ZipFile

socket.setdefaulttimeout(50)

class BhavCopy(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Bhavcopy()
        self.ui.setupUi(self)
        
        self.ui.endDate.setDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.startDate.setDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.endDate.setMaximumDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.startDate.setMaximumDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.cancelButton.setDisabled(True)

        # Create thread object and connect its signals to methods on this object
        self.ponderous = PonderousTask()
        self.connect(self.ponderous, QtCore.SIGNAL("updategui(PyQt_PyObject)"), self.appendUpdates)
        self.connect(self.ponderous, QtCore.SIGNAL("finished()"), self.downloadComplete)
        
        QtCore.QObject.connect(self.ui.downloadButton, QtCore.SIGNAL("clicked()"), self.startDownload)
        QtCore.QObject.connect(self.ui.cancelButton, QtCore.SIGNAL("clicked()"), self.cancelDownload)
        
        # Method called asynchronously by other thread when progress should be updated
    def appendUpdates(self, update):
        print update
        self.ui.progressUpdate.setText(self.ui.progressUpdate.text()+update+"\n")
        self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())

    def startDownload(self):
        self.ui.downloadButton.setDisabled(True)
        self.ui.cancelButton.setEnabled(True)
        self.ui.startDate.setDisabled(True)
        self.ui.endDate.setDisabled(True)
        startdate = str(self.ui.startDate.date().toString("dd-MM-yyyy"))
        enddate = str(self.ui.endDate.date().toString("dd-MM-yyyy"))
        self.ponderous.goNow(startdate, enddate)

    def cancelDownload(self):
        self.ponderous.stopTask()
        self.ui.downloadButton.setEnabled(True)
        self.ui.cancelButton.setDisabled(True)
        self.ui.startDate.setEnabled(True)
        self.ui.endDate.setEnabled(True)
        
    def downloadComplete(self):
        self.ui.downloadButton.setEnabled(True)
        self.ui.cancelButton.setDisabled(True)
        self.ui.startDate.setEnabled(True)
        self.ui.endDate.setEnabled(True)

class PonderousTask(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
 
    # Call this to launch the thread
    def goNow(self,startDate,endDate):
        self.startdate = startDate
        self.enddate = endDate
        self.start()

    # This run method is called by Qt as a result of calling start()
    def run(self):
        self.stopping = False
        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "-------Starting the data download-------")
        self.stopping = False
        
        br = Browser()
        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        #Emulate a Mozilla Firefox 4.0 Browser to avoid the 403 Permission Denied Error
        br.addheaders = [('Host','www.nseindia.com'),('User-Agent',' Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20100101 Firefox/4.0'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Language',' en-us,en;q=0.5'),('Accept-Charset',' ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Keep-Alive','115'),('Connection',' keep-alive')]
        
        startdate = datetime.datetime.strptime(self.startdate, '%d-%m-%Y').date()
        enddate = datetime.datetime.strptime(self.enddate, '%d-%m-%Y').date()
        
        d = startdate
        delta = datetime.timedelta(days=1)
        while d <= enddate:
                flag=0
                date = d.strftime("%d-%m-%Y")
                self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "-------"+date+"-------")
                res = br.open("http://www.nseindia.com/archives/archives.jsp?date="+date+"&fileType=eqbhav")
                #If EOD data for the given date exists, download the file by following the first link
                for link in br.links():
                    rlink = "http://nseindia.com"+link.url
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: Downloading bhavcopy...")
                    urldata = urllib.urlretrieve(rlink,None)#,reporthook)
                    
                    #Flag to mark successfull download of file.
                    flag=1
                    if(self.stopping):
                        return
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: Bhavcopy succesfully fetched!")
                    break
                     
                if(flag):
                    file = ZipFile(urldata[0], "r")
                    data  = file.read(file.namelist()[0])
                    file.close()
                    #delete the temp file created
                    urllib.urlcleanup()

                    x = data.split('\n')
                    
                    nfile= d.strftime("%d-%m-%Y") + ".txt"
                    
                    with open(nfile, 'w') as f:
                        for x1 in x[1:-1]:
                            x1 = x1.split(',')
                            #Extract and write only the EQ series data in the file
                            if(x1[1]=='EQ'):
                                try:
                                    f.write(x1[0] + "," + d.strftime("%Y%m%d") + "," + x1[2] + "," + x1[3] + "," + x1[4] + "," + x1[5] + "," + x1[8] + "\r\n")
                                except:
                                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: Error in downloading Bhavcopy.Kindly retry later.")

                        indexList = ['NSENIFTY','NIFTYJUNIOR','BANKNIFTY','NSEMIDCAP','NSEIT','NSE100','NSE500','MIDCAP50','VIX']#,'NSEDEFTY',]
                        #Create a dictionary mapping index to the index data URL
                        urls = {}
                        urls['NSENIFTY'] = 'http://nseindia.com/content/indices/histdata/S&P%20CNX%20NIFTYdate-date.csv'
                        urls['NIFTYJUNIOR'] = 'http://nseindia.com/content/indices/histdata/CNX%20NIFTY%20JUNIORdate-date.csv'
                        urls['NSE100'] = 'http://nseindia.com/content/indices/histdata/CNX%20100date-date.csv'
                        urls['NSE500'] = 'http://nseindia.com/content/indices/histdata/S&P%20CNX%20500date-date.csv'
                        urls['MIDCAP50'] = 'http://nseindia.com/content/indices/histdata/NIFTY%20MIDCAP%2050date-date.csv'
                        urls['NSEMIDCAP'] = 'http://nseindia.com/content/indices/histdata/CNX%20MIDCAPdate-date.csv' 
                        urls['BANKNIFTY'] = 'http://nseindia.com/content/indices/histdata/BANK%20NIFTYdate-date.csv' 
                        urls['NSEIT'] = 'http://nseindia.com/content/indices/histdata/CNX%20ITdate-date.csv'
                        urls['VIX'] = 'http://www.nseindia.com/content/vix/histdata/hist_india_vix_date_date.csv'
                        for index in indexList:
                            #Check whether we've been cancelled or not
                            if self.stopping:
                                return
                            newurl = re.sub('date',date,urls[index])
                            self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: Downloading "+index+ " index data...")
                            try:
                                res = br.open(newurl)
                            except:
                                self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: Error in downloading "+index+ " index data.Kindly retry later.")
                            else:
                                data = res.read()
                                abc = re.sub("\"",'',data).split(',')
                                a = []  
                                for i in abc[1:]:
                                    a.append(i.strip())
                                try:
                                    f.write(index + "," + d.strftime("%Y%m%d") + "," + a[0] + "," + a[1] + "," + a[2] + "," + a[3] + "," + a[4] + "," + a[5] + "\r\n")
                                except IOError:
                                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: Error in downloading "+index+ " index data.Kindly retry later.")
                            time.sleep(0.5)

                    f.close()
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: File successfully written.\n\n")
                else:
                    self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "Log Message: No Data Found!.\n\n")
                time.sleep(0.5)
                d += delta
        self.emit(QtCore.SIGNAL("updategui(PyQt_PyObject)"), "--------Download Complete--------")
        self.emit(QtCore.SIGNAL("finished()"))
        
    def stopTask(self):
        self.stopping = True

#Start the program
app = QtGui.QApplication(sys.argv)
window = BhavCopy()
window.show()
sys.exit(app.exec_())