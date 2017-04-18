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
            title = rank.db
            #print (page[0], page[1])
            item = (page[0], page[1])
            top_pages.append(item)
    return top_pages

def write_csv(results, filename):
    csvfile = open(filename, 'w')
    wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    data = []
    for result in results:
        data.append(result[1]) 
    wr.writerow(data)

def deal_with_boolean(results):
    matches = []
    for result in results:
        matches.append(result[1])
    return matches

def get_rank(x):
    if x == 1:
        return TFIDFRanking()
    elif x == 2:
        return BM25Ranking()
    else:
        return QueryLikelihoodRanking()

def pagerank_contrib(results):
    # get doc_id of certain result
    # multiply that doc_id with the pagerank of that doc_id
    rank = Ranking()
    sorted_results = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)
    PR_result = dict()
    for result in sorted_results:
        pagerank = rank.db.get_pagerank(result[0])
        if pagerank is None:
            item = result[1]
        else:
            item = result[1] * float(pagerank)
        PR_result[result[0]] = item
    return PR_result

if __name__ == "__main__":
    max_results = 30
    #ranking = BooleanRanking()
    while True:
        raw_ranking = raw_input("""Select the ranking algorithm you want to use: 
                \n (1) TFIDF
                \n (2) BM25
                \n (3) Query Likelihood
                \n
                \n Enter number here: """)
        ranking = get_rank(raw_ranking)
        pagerank = raw_input("Do you want it with PageRank? Y/N \n")

        raw_query_terms = raw_input("Enter a search query: ")
        query_terms = processQueryTerms(raw_query_terms)

        print "Searching for ", query_terms
        results = ranking.rankDocuments(query_terms)
        if pagerank == "Y" or "yes" or "y":
            results = pagerank_contrib(results)
        matches = get_top_docs(results, max_results)
        #matches = deal_with_boolean(results)
        # print matches
        if pagerank == "Y" or "yes" or "y":
            write_csv(matches, ("./results/" + ranking.__class__.__name__ + "_PR_" + query_terms[0]+ ".csv"))
        else:
            write_csv(matches, ("./results/" + ranking.__class__.__name__ + "_" + query_terms[0]+ ".csv"))

        print ("Results")
        for match in matches:
            print "\t" + cleanTitle(match[0]) + "\n\t\t"+ match[1]
