import psycopg2
import csv
import operator
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from app.ranking import Ranking
from app.boolean.boolean_ranking import BooleanRanking
from app.query_likelihood.query_likelihood_ranking import QueryLikelihoodRanking
from app.BM25.bm25 import BM25Ranking
from app.TFIDF.tf_idf import TFIDFRanking

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

def cleanTitle(title):
    if title[0] == '{' and title[len(title)-1] == '}':
        title = title[1:len(title)-1]
    if title[0] == '"' and title[len(title)-1] == '"':
        title = title[1:len(title)-1]
    return title

def get_top_docs(results, max_results):
    rank = Ranking()
    top_results = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)[:max_results]
    top_pages = []
    for result in top_results:
        if result[1] > 0:
            page = rank.db.get_site_by_id(result[0])
            # print (page[1], result[1])
            top_pages.append(page[1])
    return top_pages

def write_csv(results, filename):
    csvfile = open(filename, 'w')
    wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    
    #for row in results:    
    wr.writerow(results)

if __name__ == "__main__":
    max_results = 10
    #ranking = QueryLikelihoodRanking()
    ranking = BM25Ranking()
    # ranking = TFIDFRanking()
    while True:
        raw_query_terms = raw_input("Enter a search query: ")
        query_terms = processQueryTerms(raw_query_terms)

        print "Searching for ", query_terms
        results = ranking.rankDocuments(query_terms)
        matches = get_top_docs(results, max_results)
        print matches
        write_csv(matches, ("./results/BM25Ranking_" + query_terms[0]+ ".csv"))

        #print ("Results")
        #for match in matches:
         #       print ("\t", cleanTitle(match[0]), "\n\t\t", match[1])
