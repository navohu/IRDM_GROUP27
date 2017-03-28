import urllib2
import html2text
import sys  
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

reload(sys)  
sys.setdefaultencoding('utf8')

# Read from url
resp = urllib2.urlopen('http://ucl.ac.uk')
html = resp.read()

# Convert html to text
soup = BeautifulSoup(html, 'html.parser')
[s.extract() for s in soup('script')]
[s.extract() for s in soup('style')]
text = soup.get_text()

# Stopping
stop = set(stopwords.words('english'))
stopped_text = [i for i in text.lower().split() if i not in stop]

# Stemming
porter_stemmer = PorterStemmer()
stemmed_text = [porter_stemmer.stem(i) for i in stopped_text]

print stemmed_text

