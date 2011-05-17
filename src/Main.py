from subprocess import call
import os
import mechanize,urllib
import datetime
from datetime import date
import time

br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
#br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('Host','www.nseindia.com'),('User-Agent',' Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20100101 Firefox/4.0'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Language',' en-us,en;q=0.5'),('Accept-Charset',' ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Keep-Alive','115'),('Connection',' keep-alive')]

startdate=date(2011,04,25)
enddate=date(2011,04,29)
d = startdate
delta = datetime.timedelta(days=1)

while d <= enddate:
    date = d.strftime("%d-%m-%Y")
    res = br.open("http://www.nseindia.com/archives/archives.jsp?date="+date+"&fileType=eqbhav")
    data = res.read()
    for link in br.links():
        rlink = "http://nseindia.com"+link.url
        urllib.urlretrieve(rlink,date+".zip")
        print "File fetched!"
        break
    call(["unzip", "-oq", os.getcwd()+"/"+date+".zip"])
    call(["rm", os.getcwd()+"/"+date+".zip"])
    
    files=os.listdir(".")
    files=[filename for filename in files if filename[-4:] == '.csv']

    f = open(os.getcwd()+"/"+files[0], 'r')
    x = f.readlines()
    f.close()
    
    nfile= d.strftime("%d-%m-%Y") + ".txt"
    print nfile
    f = open(nfile, 'w')
    for x1 in x[1:]:
        x1 = x1.split(',')
        f.write(x1[0] + "," + d.strftime("%Y%m%d") + "," + x1[2] + "," + x1[3] + "," + x1[4] + "," + x1[5] + "," + x1[8] + "\n")
    f.close()
    call(["rm", os.getcwd()+"/"+files[0]])
    time.sleep(2)
    d += delta