from pyspark import SparkContext, SQLContext
from simple_index import InvertedIndex
from properties import properties, db_url

sc = SparkContext()
sqlContext = SQLContext(sc)
index = InvertedIndex(sc)
nextID = 1
documents = ["test-words.txt", "test-words-2.txt", "test-words-3.txt", "test-words-4.txt", "test-words.txt"]
for d in documents:
	index.addDocument(sc.textFile(d), nextID)
	nextID += 1

index.writeToDatabase(sqlContext, db_url, properties)
