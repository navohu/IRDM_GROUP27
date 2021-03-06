import csv
import psycopg2
from psycopg2.extensions import AsIs

class PostIndexing():
    def __init__(self, db='search_engine_db', usr='group27', host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com', port='5432'):
        self.conn = psycopg2.connect(dbname=db, user=usr, host=host, port=port)
        self.cur = self.conn.cursor()
        self.sites = "cs_sites"
        self.dict = "cs_dictionary_raw"
        self.occs = "cs_word_occurrences_raw"

    def close(self):
        self.cur.close()
        self.conn.close()

    def query(self, query, params=(), print_query=True, commit=True):
        self.cur.execute(query, params)
        if print_query:
            print self.cur.query
        if commit:
            self.conn.commit()

    def add_doc_lengths(self, col_name):
        self.query("""ALTER TABLE %(sites)s ADD COLUMN %(col)s BIGINT""",
                   params={"sites": AsIs(self.sites), "col": AsIs(col_name)})

        self.query("""CREATE TABLE temp_lengths AS (SELECT sum(occurrences), document_id FROM %(occs)s GROUP BY document_id)""",
                   params={"occs": AsIs(self.occs)})

        self.query("""UPDATE %(sites)s SET %(col)s = sum FROM temp_lengths WHERE %(sites)s.id = temp_lengths.document_id""",
                  params={"sites": AsIs(self.sites), "col": AsIs(col_name)})

        self.query("DROP TABLE temp_lengths")

    def add_word_freqs(self, col_name):
        self.query("""ALTER TABLE %(dict)s ADD COLUMN %(col)s BIGINT""",
                   params={"dict": AsIs(self.dict), "col": AsIs(col_name)})

        self.query("""CREATE TABLE temp_freqs AS (SELECT sum(occurrences), word_id FROM %(occs)s GROUP BY word_id)""",
                   params={"occs": AsIs(self.occs)})

        self.query("""UPDATE %(dict)s SET %(col)s = sum FROM temp_freqs WHERE %(dict)s.word_id = temp_freqs.word_id""",
                   params={"dict": AsIs(self.dict), "col": AsIs(col_name)})

        self.query("DROP TABLE temp_freqs")

    def add_pageranks(self, pageranks):
        with open("pageranks.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(pageranks)

        self.query("""CREATE TABLE temp_pageranks(link VARCHAR, rank NUMERIC)""")
        with open("pageranks.csv", "r") as f:
            self.cur.copy_from(f, 'temp_pageranks', sep=",")
        
        self.query("""ALTER TABLE %(sites)s ADD COLUMN pagerank NUMERIC""",
                   params={"sites": AsIs(self.sites)})
        self.query("""UPDATE %(sites)s SET pagerank = rank FROM temp_pageranks WHERE %(sites)s.link = temp_pageranks.link""",
                   params={"sites": AsIs(self.sites)})
        self.query("""DROP TABLE temp_pageranks""")


if __name__ == "__main__":
    post_indexing = PostIndexing()
    post_indexing.add_doc_lengths("raw_length")
    post_indexing.add_word_freqs("freq")
    post_indexing.close()



