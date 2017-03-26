from pyspark import SparkContext

def addSourceID(word, nextID):
	return (word, (nextID, 1))

def flattenTuple(t):
	if type(t) == tuple and len(t) > 0 and type(t[0]) == tuple and len(t[0]) > 0 and type(t[0][0]) == tuple:
		l = list(t[0])
		l.append(t[1])
		return tuple(l)
	return t

class InvertedIndex:
	def __init__(self, sc):
		self.invertedIndex = sc.emptyRDD()

	def addDocument(self, websiteText, nextID):
		# Count words in current document and map them to document ID
		wordSources = websiteText.flatMap(lambda line: line.split()) \
			.map(lambda word: addSourceID(word, nextID)) \
			.reduceByKey(lambda a, b: (a[0], a[1]+b[1]))

		# Add words from current document to inverted index
		self.invertedIndex = self.invertedIndex.union(wordSources) \
			.reduceByKey(lambda a, b: (a, b)) \
			.map(lambda kv_pair: (kv_pair[0], flattenTuple(kv_pair[1])))

		print self.invertedIndex.collect()

	def writeToDatabase():
		# TODO
		pass