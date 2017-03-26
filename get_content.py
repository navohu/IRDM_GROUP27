import urllib2
import html2text
import sys  
from bs4 import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf8')
resp = urllib2.urlopen('http://ucl.ac.uk')
html = resp.read()
soup = BeautifulSoup(html, 'html.parser')
[s.extract() for s in soup('script')]
print(soup.get_text())