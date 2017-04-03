import psycopg2

try:
    conn = psycopg2.connect("dbname='search_engine_db' user='group27' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port=5432")
except:
    print "Unable to connect to the database"

cur = conn.cursor()

#while True:
query_terms = ['ucl', 'student']
#query_terms = raw_input("Enter a search query: ").split()
#for term in query_terms:
print """SELECT word, word_id FROM cs_dictionary WHERE word IN %s"""% query_terms 

cur.execute("""SELECT word, word_id FROM cs_dictionary WHERE word = ANY(%s)""", (query_terms,))
rows = cur.fetchall()

for row in rows:
    print "   ", row
