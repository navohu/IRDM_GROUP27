import psycopg2
import sys
import json

con = None

with open("./crawl/cs.json") as data_file:    
    data = json.load(data_file)

try:
     
    con = psycopg2.connect("dbname='search_engine_db' user='group27' password='' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port='5432'")   
    
    cur = con.cursor()
    
    cur.execute("DROP TABLE cs_sites")
    cur.execute("CREATE TABLE cs_sites(Id INTEGER PRIMARY KEY, Title VARCHAR(20), Link VARCHAR(20))")
    i = 0
    for site in data:
        cur.execute("INSERT INTO cs_sites VALUES(%i, %s, %s)", (i, site["title"],site["link"]))
        i = i+1
    
    
    con.commit()
    

except psycopg2.DatabaseError, e:
    
    if con:
        con.rollback()
    
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()