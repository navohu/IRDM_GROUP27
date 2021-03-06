import psycopg2
from bs4 import BeautifulSoup
import urllib2
import sys
import requests
from db import MyDB

class MyDB():
    def __init__(self, db='search_engine_db', usr='group27', p='',host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com', port='5432'):
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

def write_to_json(feeds, obj):
    with open('graph.json', mode='w', encoding='utf-8') as feedsjson:
        feeds.append(obj)
        json.dump(feeds, feedsjson)


def get_graph(urls, feeds):
    graph = {}
    for key in urls:
        resp = requests.get(key[0])
        encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        soup = BeautifulSoup(resp.content, from_encoding=encoding)
        llinks = [] 
        for link in soup.find_all('a', href=True): 
            if "www." in link['href']: 
                llinks.append(link['href'])
        graph[key[0]] = llinks
        obj = {key[0]:llinks}
        print obj
        write_to_json(feeds, obj)
    return graph

def main():
    with open('graph.json', mode='r', encoding='utf-8') as feedsjson:
        feeds = json.load(feedsjson)

    urls = fetch_database_urls()
    graph = get_graph(urls, feeds)

if __name__ == '__main__':
    main()

