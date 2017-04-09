class MyDB():
    def __init__(self, db='search_engine_db', usr='group27', p='',host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com', port='5432'):
        self.conn = psycopg2.connect(dbname=db, user=usr, password=p, host = host, port= port)
        self.cur = self.conn.cursor()

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
        pass

    def get_term_freq_doc(self, query, doc):
        pass

    def get_term_freq_collection(self,query,collection):
        pass