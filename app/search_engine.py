import psycopg2
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from app.boolean.boolean_ranking import BooleanRanking

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

if __name__ == "__main__":
    max_results = 10
    ranking = BooleanRanking()
    while True:
        raw_query_terms = raw_input("Enter a search query: ")
        query_terms = processQueryTerms(raw_query_terms)
        print "Searching for ", query_terms
        matches = ranking.rankDocuments(query_terms, max_results)

        print "Results"
        for match in matches:
                print "\t", cleanTitle(match[0]), "\n\t\t", match[1]
