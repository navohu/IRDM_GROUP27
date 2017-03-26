import psycopg2
import sys

con = None
import json

with open("./crawl/cs.json") as data_file:    
    data = json.load(data_file)

try:
     
    con = psycopg2.connect("dbname='search_engine_db' user='group27' password='' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port='5432'")   
    
    cur = con.cursor()
    
    cur.execute("CREATE TABLE cs_sites(Title VARCHAR(20), Link VARCHAR(20))")
    
    for site in data:
        cur.execute("INSERT INTO cs_sites VALUES(site["title"],site["link"])")
    
    
    con.commit()
    

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()