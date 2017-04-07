import psycopg2
from bs4 import BeautifulSoup
import urllib2
import sys
import requests

class MyDB():
    def __init__(self, db='search_engine_db', usr='group27', p='irdm.group27',host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com', port='5432'):
        self.conn = psycopg2.connect(dbname=db, user=usr, password=p, host = host, port= port)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()



def fetch_database_urls():
    db = MyDB()
    query = "SELECT link, id FROM cs_sites"
    db.query(query)
    urls = {}
    for item in list(db.fetchall()):
        urls[item[1]] = item[0]
    db.commit()
    db.close()
    return urls


def get_urls(urls):
    db = MyDB()
    for key, value in urls.iteritems():
        print key
        print value
        resp = requests.get(value)
        encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(resp.content, from_encoding=encoding)

        for link in soup.find_all('a', href=True):
            if "www." in link['href']:
                # url = the source
                # link['href'] = one outgoing link
                query1 = """
                        INSERT INTO cs_outgoing(link)
                        VALUES("%s")
                        WHERE NOT EXISTS (SELECT * FROM cs_outgoing WHERE link = "%s")

                """
                query2 = "INSERT INTO cs_graph VALUES(%s, SELECT TOP 1 Id FROM cs_outgoing WHERE Link = %s)"
                db.query(query1 % (link['href'], link['href']))
                db.commit()
                db.query(query2 % (key, link['href']))
                db.commit()
    db.close()

# llinks.append(link['href'])
# json[url] = llinks
# write_url_database(url, json[url])
# return json

def main():
    #db = MyDB()
    #create_graph = "CREATE TABLE cs_graph(Id serial, Link VARCHAR(1000) PRIMARY KEY , Outgoing VARCHAR(1000))"
    #create_outgoing = "CREATE TABLE cs_outgoing(Id serial PRIMARY KEY, Link VARCHAR(1000))"
    #db.query(create_graph)
    #db.query(create_outgoing)
    #db.commit()
    #db.close()

    urls = fetch_database_urls()
    get_urls(urls)



if __name__ == '__main__':
    main()

