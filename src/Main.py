import mechanize,urllib
br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
#br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('Host','www.nseindia.com'),('User-Agent',' Mozilla/5.0 (X11; Linux i686; rv:2.0) Gecko/20100101 Firefox/4.0'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Language',' en-us,en;q=0.5'),('Accept-Charset',' ISO-8859-1,utf-8;q=0.7,*;q=0.7'),('Keep-Alive','115'),('Connection',' keep-alive')]
res = br.open("http://www.nseindia.com/archives/archives.jsp?date=10-05-2011&fileType=eqbhav")
data = res.read()
for link in br.links():
    rlink = "http://nseindia.com"+link.url
    urllib.urlretrieve(rlink, "abc.zip")
    break