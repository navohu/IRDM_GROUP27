import psycopg2
from psycopg2.extensions import AsIs

class PostIndexing():
    def __init__(self, db='search_engine_db', usr='group27', host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com', port='5432'):
        self.conn = psycopg2.connect(dbname=db, user=usr, host=host, port=port)
        self.cur = self.conn.cursor()
        self.sites = "cs_sites"
        self.dict = "cs_dictionary"
        self.occs = "cs_word_occurrences"

    def close(self):
        self.cur.close()
        self.conn.close()

    def query(self, query, params=()):
        self.cur.execute(query, params)
        print self.cur.query
        self.conn.commit()

    def add_doc_lengths(self, col_name):
        self.query("""ALTER TABLE %(sites)s ADD COLUMN %(col)s INTEGER""",
                   params={"sites": AsIs(self.sites), "col": AsIs(col_name)})

        self.query("""CREATE TABLE temp_lengths AS (SELECT sum(occurrences), document_id FROM %(occs)s GROUP BY document_id)""",
                   params={"occs": AsIs(self.occs)})

        self.query("""UPDATE %(sites)s SET %(col)s = sum FROM temp_lengths WHERE %(sites)s.id = temp_lengths.document_id""",
                  params={"sites": AsIs(self.sites), "col": AsIs(col_name)})

        self.query("DROP TABLE temp_lengths")

    def add_word_freqs(self, col_name):
        self.query("""ALTER TABLE %(dict)s ADD COLUMN %(col)s INTEGER""",
                   params={"dict": AsIs(self.dict), "col": AsIs(col_name)})

        self.query("""CREATE TABLE temp_freqs AS (SELECT sum(occurrences), word_id FROM %(occs)s GROUP BY word_id)""",
                   params={"occs": AsIs(self.occs)})

        self.query("""UPDATE %(dict)s SET %(col)s = sum FROM temp_freqs WHERE %(dict)s.word_id = temp_freqs.word_id""",
                   params={"dict": AsIs(self.dict), "col": AsIs(col_name)})

        self.query("DROP TABLE temp_freqs")


if __name__ == "__main__":
    post_indexing = PostIndexing()
    post_indexing.add_doc_lengths("stemmed_length")
    post_indexing.add_word_freqs("freq")
    post_indexing.close()



