import psycopg2
from psycopg2.extensions import AsIs

class MyDB():
    def __init__(self, db='search_engine_db', usr='group27', host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com', port='5432'):
        self.conn = psycopg2.connect(dbname=db, user=usr, host=host, port=port)
        self.cur = self.conn.cursor()
        self.sites = "cs_sites"
        self.dict = "cs_dictionary"
        self.occs = "cs_word_occurrences"

    def query(self, query, params=()):
        self.cur.execute(query, params)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_doc_length(self, doc):
        self.query("""SELECT stemmed_length FROM %(occs)s AS o JOIN %(sites)s AS s ON o.document_id = s.id WHERE link = %(doc)s""",
                params={"occs": AsIs(self.occs), "sites": AsIs(self.sites), "doc": doc})
        return self.cur.fetchone()[0]

    def get_term_freq_doc(self, query_term, url):
        self.query("""SELECT occurrences FROM (%(occs)s AS o JOIN %(sites)s AS s ON o.document_id = s.id) AS os JOIN %(dict)s AS d ON d.word_id = os.word_id WHERE d.word = %(term)s AND os.link = %(url)s""",
                params={"occs": AsIs(self.occs), "sites": AsIs(self.sites), "dict": AsIs(self.dict), "term": query_term, "url": url})
        return self.cur.fetchone()[0]

    def get_term_freq_collection(self, query_term):
        self.query("""SELECT freq FROM %(dict)s WHERE word = %(term)s""",
                params={"dict": AsIs(self.dict), "term": query_term})
        return self.cur.fetchone()[0]

if __name__ == "__main__":
    '''Testing'''
    db = MyDB()
    print db.get_doc_length("http://www.cs.ucl.ac.uk/mobile/home/")
    print db.get_term_freq_doc('ucl', "http://www.cs.ucl.ac.uk/mobile/home/")
    print db.get_term_freq_collection('ucl')