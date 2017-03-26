from pyspark import SparkContext
from simple_index import InvertedIndex

sc = SparkContext()
index = InvertedIndex(sc)
nextID = 0
documents = ["test-words.txt", "test-words-2.txt", "test-words-3.txt", "test-words-4.txt", "test-words.txt"]
for d in documents:
	index.addDocument(sc.textFile(d), nextID)
	nextID += 1