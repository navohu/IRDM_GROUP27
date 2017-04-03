import psycopg2

try:
    conn = psycopg2.connect("dbname='search_engine_db' user='group27' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port=5432")
except:
    print "Unable to connect to the database"

cur = conn.cursor()

while True:
    #query_terms = ['ucl', 'student']
    query_terms = raw_input("Enter a search query: ").split()

    cur.execute("""SELECT word_id FROM cs_dictionary WHERE word = ANY(%s)""", (query_terms,))
    rows = cur.fetchall()

    '''print "\tWord IDs"
    for row in rows:
        print "\t", row
    '''

    cur.execute("""SELECT document_id FROM cs_word_occurrences WHERE word_id = ANY(%s)""", (rows,))
    docs = cur.fetchall()

    '''print "\tDoc IDs"
    for doc in docs:
        print "\t", doc
    '''

    cur.execute("""SELECT link FROM cs_sites WHERE id = ANY(%s)""", (docs,))
    urls = cur.fetchmany(5)
    print "Results"
    for url in urls:
        print "\t", url
