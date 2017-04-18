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

import time

class SearchEngine():

    def processQueryTerms(self, query_terms):
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

    def cleanTitle(self, title):
        if title[0] == '{' and title[len(title)-1] == '}':
            title = title[1:len(title)-1]
        if title[0] == '"' and title[len(title)-1] == '"':
            title = title[1:len(title)-1]
        return title

    def get_top_docs(self, results, max_results, rank):
        top_results = sorted(results.iteritems(), key=operator.itemgetter(1), reverse=True)[:max_results]
        site_ids = [result[0] for result in top_results]
        top_pages = []
        urls = dict(rank.db.get_site_links(site_ids))
        titles = dict(rank.db.get_site_titles(site_ids))

        for result in top_results:
            page_id = result[0]
            relevance = result[1]
            if relevance > 0.0:
                url = urls[page_id]
                title = titles[page_id]
                #print (page[0], page[1])
                item = (title, url)
                top_pages.append(item)
        return top_pages

    def write_csv(self, results, filename, perm):
        csvfile = open(filename, perm)
        wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        data = []
        for result in results:
            data.append(result[1]) 
        wr.writerow(data)

    def deal_with_boolean(self, results):
        matches = []
        for result in results:
            matches.append(result[1])
        return matches

    def get_rank(self, x):
        x = int(x)
        if x == 1:
            return TFIDFRanking()
        elif x == 2:
            return BM25Ranking()
        else:
            return QueryLikelihoodRanking()

    def pagerank_contrib(self, results, rank):
        # get doc_id of certain result
        # multiply that doc_id with the pagerank of that doc_id
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

    def add_pageranks(self, pageranks, results):
        PR_results = results
        for result in results.iteritems():
            page_id = result[0]
            relevance = result[1]
            if page_id in pageranks and pageranks[page_id] is not None:
                PR_results[page_id] = relevance * float(pageranks[page_id])
        return PR_results

if __name__ == "__main__":
    max_results = 30
    max_printed = 10
    raw_ranking = raw_input("""Select the ranking algorithm you want to use: 
                            \n (1) TFIDF
                            \n (2) BM25
                            \n (3) Query Likelihood
                            \n
                            \n Enter number here: """)
    search = SearchEngine()
    ranking = search.get_rank(raw_ranking)
    pagerank = raw_input("Do you want it with PageRank? Y/N \n")

    if pagerank == "Y" or pagerank == "yes" or pagerank == "y":
        use_pagerank = True
        pageranks = dict(ranking.db.get_pageranks())
    else:
        use_pagerank = False

    while True:
        raw_query_terms = raw_input("Enter a search query: ")
        query_terms = search.processQueryTerms(raw_query_terms)
        print "Searching for ", query_terms

        results = ranking.rankDocuments(query_terms)
        if use_pagerank:
            results = search.add_pageranks(pageranks, results)
        matches = search.get_top_docs(results, max_results, ranking)
        #matches = deal_with_boolean(results)
        #print 'Time to fetch urls', time.time() - prev_time

        print ("Results")
        for match in matches[:max_printed]:
            print "\t" + search.cleanTitle(match[0]) + "\n\t\t"+ match[1]

        if use_pagerank:
            search.write_csv(matches, ("./results/" + ranking.__class__.__name__ + "_PR_" + query_terms[0]+ ".csv"), 'w')
        else:
            search.write_csv(matches, ("./results/" + ranking.__class__.__name__ + "_" + query_terms[0]+ ".csv"), 'w')
