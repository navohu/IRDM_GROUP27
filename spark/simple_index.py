from pyspark import SparkContext

def addSourceID(entry, ID):
	return (entry, (ID, 1))

sc = SparkContext()
documents = ["test-words.txt", "test-words-2.txt", "test-words-3.txt"]
invertedIndex = sc.emptyRDD()

for d in range(len(documents)):
	websiteText = sc.textFile(documents[d])

	wordSources = websiteText.flatMap(lambda line: line.split()) \
		.map(lambda word: addSourceID(word, d)) \
		.reduceByKey(lambda a, b: (a[0], a[1]+b[1]))

	# TODO: flatten value tuples
	invertedIndex = invertedIndex.union(wordSources) \
		.reduceByKey(lambda a, b: (a, b))

	print d+1, 'documents', invertedIndex.collect()