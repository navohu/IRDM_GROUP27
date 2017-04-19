import time
import csv
from app.ranking import Ranking
from app.search_engine import SearchEngine
from app.boolean.boolean_ranking import BooleanRanking
from app.query_likelihood.query_likelihood_ranking import QueryLikelihoodRanking
from app.BM25.bm25 import BM25Ranking
from app.TFIDF.tf_idf import TFIDFRanking

class Timing():
    def __init__(self):
        self.search = None

    def set_search_engine(self, search_engine):
        self.search = search_engine

    def write_csv(self, results, filename, perm):
        csvfile = open(filename, perm)
        wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
        data = []
        for result in results:
            data.append(result) 
        wr.writerow(data)

    def produce_time(self, queries, ranking, use_pagerank):
        timing = []
        for query in queries:
            query_terms = self.search.processQueryTerms(query)
            prev_time = time.time()
            results = ranking.rankDocuments(query_terms)
            if use_pagerank:
                pageranks = dict(ranking.db.get_pageranks())
                results = self.search.add_pageranks(pageranks, results)
            timing.append(time.time() - prev_time)
            print time.time()-prev_time
        return timing

    def produce_average(self, times):
        sum = 0
        for i in times:
            sum = sum + i
        return sum/len(times)

if __name__ == "__main__":
    queries = ["jun wang", "degree", "moodle", "alphago", "information retrieval and data mining", "computer graphics syllabus", "ai research", "new research", "emine yilmaz", "computational complexity"]
    timing = Timing()
    rankings = [BooleanRanking(), BM25Ranking(), TFIDFRanking(), QueryLikelihoodRanking()]
    use_pagerank = False
    for ranking in rankings:
        timing.set_search_engine(SearchEngine(ranking))
        name = ranking.__class__.__name__
        print name
        times =  timing.produce_time(queries, ranking, use_pagerank)
        avg = timing.produce_average(times)
        print avg
        item = (name,avg)
        if use_pagerank:
            timing.write_csv(item, "./results/time/timing_" + "PR.csv", 'a')
        else:
            timing.write_csv(item, "./results/time/timing" + ".csv", 'a')

