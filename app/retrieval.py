import psycopg2
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def connectToPostgres():
    try:
        conn = psycopg2.connect("dbname='search_engine_db' user='group27' host='searchengineindex.cwbjh0hhu9l3.us-west-2.rds.amazonaws.com' port=5432")
    except:
        print "Unable to connect to the database"

    return conn.cursor()

def processQueryTerms(query_terms):
    stop = set(stopwords.words('english'))
    stopped_terms = [i for i in query_terms.lower().split() if i not in stop]

    # Stemming
    porter_stemmer = PorterStemmer()
    stemmed_terms = [porter_stemmer.stem(i) for i in stopped_terms]

    final_terms = [] 
    for word in stemmed_terms:
        word = word.replace(u'\00', '')
        # Split hyphenated words
        for w in word.split('-'):
            # Trim punctuation
            alphanum = filter(unicode.isalnum, w)
            final_terms.append(alphanum)
    return final_terms

def documentsWithAnyTerm(cur, query_terms, excluded_urls=[], count=5):
        if len(excluded_urls) == 0:
            cur.execute("""SELECT title, link FROM (cs_dictionary AS d JOIN cs_word_occurrences AS w ON w.word_id = d.word_id) AS wd JOIN cs_sites AS s ON s.id = wd.document_id WHERE word = ANY(%s)""", (query_terms,))
        else:
            cur.execute("""SELECT title, link FROM (cs_dictionary AS d JOIN cs_word_occurrences AS w ON w.word_id = d.word_id) AS wd JOIN cs_sites AS s ON s.id = wd.document_id WHERE word = ANY(%s) AND NOT s.link = ANY(%s)""", (query_terms, excluded_urls))
        return cur.fetchmany(count)
    
def documentsWithAllTerms(cur, query_terms, count=5):
        #cur.execute("""SELECT word_id, document_id, occurrences FROM cs_dictionary AS d JOIN cs_word_occurrences AS w ON d.word_id = w.word_id WHERE word = ANY(%s)""", (query_terms,))
        #occs = cur.fetchall()
        cur.execute("""SELECT title, link FROM (SELECT w.word_id, document_id, occurrences FROM cs_dictionary AS d JOIN cs_word_occurrences AS w ON d.word_id = w.word_id WHERE word = ANY(%s)) AS wd JOIN cs_sites AS s ON wd.document_id = s.id GROUP BY document_id, title, link HAVING count(word_id) = %s""", (query_terms, len(query_terms),))
        return cur.fetchmany(count)

if __name__ == "__main__":
        max_results = 10
        cur = connectToPostgres()
        while True:
                raw_query_terms = raw_input("Enter a search query: ")#.split()
                query_terms = processQueryTerms(raw_query_terms)
                print "Searching for ", query_terms
                matches = documentsWithAllTerms(cur, query_terms, max_results)
                match_count = len(matches)
                if match_count < max_results:
                        excluded_urls = [m[1] for m in matches]
                        loose_matches = documentsWithAnyTerm(cur, query_terms, excluded_urls, max_results - match_count)
                        for m in loose_matches:
                            matches.append(m)
                print "Results"
                for match in matches:
                        print "\t", match[0], "\t", match[1] 
