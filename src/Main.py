#TODO: Handle incomplete file downloads due to net disconnection.
#TODO: Handle incomplete file written on the disk due to abrupt program exit.
#TODO: Handle no internet connection with a timeout
#TODO: Individual Time out for different Index data downloads
#TODO: VIX URL still UNKOWN
#TODO: Delete the files from the temp directory
#TODO: Multithread GUI and Downloader so that GUI doesn't hang while data is being downloaded.
#TODO: attach reporthook to progressbar
#TODO: attach display label to print commands
from PyQt4 import QtCore, QtGui
from gui import  Ui_Bhavcopy
import sys

def download(startdate, enddate):
    from datetime import date,datetime
    import mechanize,urllib
    import time, re
    from zipfile import ZipFile
    
    br = mechanize.Browser()
    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    #Emulate a Mozilla Firefox 4.0 Browser to avoid the 403 Permission Denied Error
    br.addheaders = [('Host','www.nseindia.com'),('User-Agent',' Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20100101 Firefox/4.0'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Language',' en-us,en;q=0.5'),('Accept-Charset',' ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Keep-Alive','115'),('Connection',' keep-alive')]
    
    startdate = datetime.datetime.strptime(startdate, '%d-%m-%Y').date()
    enddate = datetime.datetime.strptime(enddate, '%d-%m-%Y').date()
    
    d = startdate
    
    delta = datetime.timedelta(days=1)
    while d <= enddate:
            flag=0
            date = d.strftime("%d-%m-%Y")
            res = br.open("http://www.nseindia.com/archives/archives.jsp?date="+date+"&fileType=eqbhav")
            def reporthook(a,b,c):
                """Download progress bar!"""
                print "% 3.1f%% of %d bytes\r" % (min(100, float(a * b) / c * 100), c),
    #            sys.stdout.flush()
            
            #If EOD data for the given date exists, download the file by following the first link
            for link in br.links():
                rlink = "http://nseindia.com"+link.url
                print "Fetching bhavcopy..."
                urldata = urllib.urlretrieve(rlink,None,reporthook)
                #Flag to mark successfull download of file.
                flag=1
                print "Bhavcopy succesfully fetched!"
                break
            
            if(flag):
                file = ZipFile(urldata[0], "r")
                data  = file.read(file.namelist()[0])
                file.close()
                x = data.split('\n')
                
                nfile= d.strftime("%d-%m-%Y") + ".txt"
                print nfile
                
                with open(nfile, 'w') as f:
                    t='junk'
                    for x1 in x[1:-1]:
                        x1 = x1.split(',')
                        stcksymb = x1[0]
                        if(stcksymb==t):
                            pass
                        else:
                            t=stcksymb
                            f.write(x1[0] + "," + d.strftime("%Y%m%d") + "," + x1[2] + "," + x1[3] + "," + x1[4] + "," + x1[5] + "," + x1[8] + "\r\n")
                    
                    
                    indexList = ['NSENIFTY','NIFTYJUNIOR','BANKNIFTY','NSEMIDCAP','NSEIT','NSE100','NSE500','MIDCAP50']#,'NSEDEFTY','VIX']
                    #Create a dictionary mapping index to the index data URL
                    urls = {}
                    urls['NSENIFTY'] = 'http://nseindia.com/content/indices/histdata/S&P%20CNX%20NIFTYdate-date.csv'
                    urls['NIFTYJUNIOR'] = 'http://nseindia.com/content/indices/histdata/CNX%20NIFTY%20JUNIORdate-date.csv'
                    urls['NSE100'] = 'http://nseindia.com/content/indices/histdata/CNX%20100date-date.csv'
                    urls['NSE500'] = 'http://nseindia.com/content/indices/histdata/S&P%20CNX%20500date-date.csv'
                    urls['MIDCAP50'] = 'http://nseindia.com/content/indices/histdata/NIFTY%20MIDCAP%205017-05-2011-18-05-2011.csv'
                    urls['NSEMIDCAP'] = 'http://nseindia.com/content/indices/histdata/CNX%20MIDCAPdate-date.csv' 
                    urls['BANKNIFTY'] = 'http://nseindia.com/content/indices/histdata/BANK%20NIFTYdate-date.csv' 
                    urls['NSEIT'] = 'http://nseindia.com/content/indices/histdata/CNX%20ITdate-date.csv'
    
                    for index in indexList:
                        newurl = re.sub('date',date,urls[index])
                        print "Downloading "+index+ " index data..."
                        urlpointer = urllib.urlretrieve(newurl,None)#,reporthook)
                        #Read the downloaded csv file 
                        f2 = open(urlpointer[0],'r')
                        data = f2.readlines()
                        f2.close()
                        
                        abc = re.sub("\"",'',data[1]).split(',')
                        a = []  
                        for i in abc[1:]:
                            a.append(i.strip())
                        f.write(index + "," + d.strftime("%Y%m%d") + "," + a[0] + "," + a[1] + "," + a[2] + "," + a[3] + "," + a[4] + "," + a[5] + "\r\n")
                    
                f.close()
                print "File successfully downloaded."
            time.sleep(2)
            d += delta
    print "DOWNLOAD COMPLETE!"

class BhavCopy(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Bhavcopy()
        self.ui.setupUi(self)
        self.ui.endDate.setDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.startDate.setDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.endDate.setMaximumDate(QtCore.QDateTime.currentDateTime().date())
        self.ui.startDate.setMaximumDate(QtCore.QDateTime.currentDateTime().date())
        
        QtCore.QObject.connect(self.ui.downloadButton, QtCore.SIGNAL("clicked()"), self.downloadButtonclicked)

    def downloadButtonclicked(self):
        print "sexy!"
        #Startdate must not be greater than the end date 
        
        self.ui.downloadButton.setDisabled(True)
        self.ui.startDate.setDisabled(True)
        self.ui.endDate.setDisabled(True)
        startdate = str(self.ui.startDate.date().toString("dd-MM-yyyy"))
        enddate = str(self.ui.endDate.date().toString("dd-MM-yyyy"))
        download(startdate, enddate)
        
if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        window = BhavCopy()
        window.show()
        sys.exit(app.exec_())