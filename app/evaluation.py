from app.search_engine import SearchEngine
from app.boolean.boolean_ranking import BooleanRanking

queries = ["information retrieval and data mining", "alphago", "computer graphics syllabus", "bioinformatics home page"]

ranking = BooleanRanking()
search = SearchEngine(ranking)
pageranks = dict(search.ranking.db.get_pageranks())
max_results = 30

for raw_q in queries:
	q = search.processQueryTerms(raw_q)
	print q
	results = search.ranking.rankDocuments(q)
	pr_results = search.add_pageranks(pageranks, results)

	matches = search.get_top_docs(results, max_results)
	search.write_csv(matches, ("./results/" + search.ranking.__class__.__name__ + "_" + q[0]+ ".csv"), 'w')

	pr_matches = search.get_top_docs(results, max_results)
	search.write_csv(pr_matches, ("./results/" + search.ranking.__class__.__name__ + "_PR_" + q[0]+ ".csv"), 'w')