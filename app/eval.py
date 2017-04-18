import pandas as pd
from sklearn.metrics import precision_recall_curve
import csv
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

def get_ground_truth(filename):
    with open(filename, 'r') as csvfile:
        data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    return data

def get_relevant():
    

def get_retrieved():


def precision(relevant, retrieved):
    return (relevant * retrieved)/retrieved

def recall(relevant, retrieved):
    return (relevant * retrieved)/relevant

if __name__ == "__main__":
    max_results = 10
    #ranking = QueryLikelihoodRanking()
    #ranking = BM25Ranking()
    ranking = TFIDFRanking()

    # while True:
    #     raw_query_terms = raw_input("Enter a search query: ")
    #     query_terms = processQueryTerms(raw_query_terms)
    #     print "Searching for ", query_terms
    #     matches = ranking.rankDocuments(query_terms, max_results)

    #     print "Results"
    #     for match in matches:
    #             print "\t", cleanTitle(match[0]), "\n\t\t", match[1]
        