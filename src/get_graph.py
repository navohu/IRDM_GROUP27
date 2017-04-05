import psycopg2
from bs4 import BeautifulSoup
import urllib2
import sys
import requests

def fetch_database_urls():
    urls = []
    try:
        con = psycopg2.connect("dbname='search_engine_db' user='group27' password='irdm.group27' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port='5432'")   
        cur = con.cursor()
        query = "SELECT link FROM cs_sites"
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
    json = {}
    for url in database:
        resp = requests.get("http://www.cs.ucl.ac.uk")
        encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(resp.content, from_encoding=encoding)

        
        llinks = []
        for link in soup.find_all('a', href=True):
            if "www." in link['href']:
                llinks.append(link['href'])
        json[url] = llinks
    return json
database_urls = fetch_database_urls()
print get_urls(database_urls)

