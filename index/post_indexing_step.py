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
        self.query("""ALTER TABLE %(sites)s ADD COLUMN pagerank NUMERIC""",
                   params={"sites": AsIs(self.sites)})
        pageranks = map(lambda row: {"url": row[0], "rank": row[1]}, pageranks)
        print pageranks[:3]
        #for pr in range(len(pageranks)):
        #    if pr % 1000 == 0:
        #        print "Writing pagerank"
        #    pagerank = {"url": pageranks[pr][0], "rank": pageranks[pr][1]}
        #    self.query("""UPDATE %(sites)s SET pagerank = %(rank)s WHERE link = %(url)s""",
        #               params={"sites": AsIs(self.sites), "url": pagerank[0], "rank": pagerank[1]},
        #               print_query=False,
        #               commit=False)
        self.cur.executemany("""UPDATE {0} SET pagerank = %(rank)s WHERE link = %(url)s""".format(self.sites),
                            pageranks)
        self.conn.commit()


if __name__ == "__main__":
    post_indexing = PostIndexing()
    post_indexing.add_doc_lengths("raw_length")
    post_indexing.add_word_freqs("freq")
    post_indexing.close()



