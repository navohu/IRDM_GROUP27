from bs4 import BeautifulSoup
import urllib2

def fetch_database_urls():
    urls = []
    try:
        con = psycopg2.connect("dbname='search_engine_db' user='group27' password='' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port='5432'")   
        cur = con.cursor()
        query = "SELECT link FROM `cs_sites`"
        cur.execute(query)

        for item in list(cur.fetchall()):
            urls.append(item[0])
        con.commit()

    except psycopg2.DatabaseError, e:
        
        if con:
            con.rollback()
        
        print 'Error %s' % e    
        sys.exit(1)

    return urls

def get_urls(database):

    for url in database:
        resp = urllib2.urlopen(url)
        soup = BeautifulSoup(resp, from_encoding=resp.info().getparam('charset'))

        for link in soup.find_all('a', href=True):
            print link['href']
        break


database_urls = fetch_database_urls()
get_urls(database_urls)

