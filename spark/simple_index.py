from pyspark import SparkContext

def addSourceID(entry, ID):
	return (entry, (ID, 1))

def flattenTuple(a):
	if type(a) == tuple and len(a) > 0 and type(a[0]) == tuple and len(a[0]) > 0 and type(a[0][0]) == tuple:
		l = list(a[0])
		l.append(a[1])
		return tuple(l)
	return a

sc = SparkContext()
documents = ["test-words.txt", "test-words-2.txt", "test-words-3.txt", "test-words-4.txt", "test-words.txt"]
invertedIndex = sc.emptyRDD()

for d in range(len(documents)):
	websiteText = sc.textFile(documents[d])

	# Count words in current document and map them to document ID
	wordSources = websiteText.flatMap(lambda line: line.split()) \
		.map(lambda word: addSourceID(word, d)) \
		.reduceByKey(lambda a, b: (a[0], a[1]+b[1]))

	# Add words from current document to inverted index
	invertedIndex = invertedIndex.union(wordSources) \
		.reduceByKey(lambda a, b: (a, b)) \
		.map(lambda kv_pair: (kv_pair[0], flattenTuple(kv_pair[1])))

	print d+1, 'documents', invertedIndex.collect()