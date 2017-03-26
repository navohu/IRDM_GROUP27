from pyspark import SparkContext
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql.functions import monotonically_increasing_id


def addSourceID(word, nextID):
	return (word, (nextID, 1))

def flattenTuple(t):
	'''Remove nested tuples (((d, f), (d, f)), (d,f )) -> ((d, f), (d, f), (d, f))'''
        if type(t) == tuple and len(t) > 0 and type(t[0]) == tuple and len(t[0]) > 0 and type(t[0][0]) == tuple:
		l = list(t[0])
		l.append(t[1])
		return tuple(l)
	return t

def splitTuple(kv_pair):
        '''Split one key value pair (word, ((docId1, count1), (docId2, count2),...)) into one (word, docId, count) tuple per document and word'''
        tuple_list = []
        if type(kv_pair[1][0]) == tuple:
                for tup in kv_pair[1]:
                        tuple_list.append((kv_pair[0], tup[0], tup[1]))
        else:
                tuple_list.append((kv_pair[0], kv_pair[1][0], kv_pair[1][1]))
        return tuple_list

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

	def writeToDatabase(self, sqlContext, url, properties):
                #sqlContext.sql("CREATE TABLE IF NOT EXISTS dictionary(word VARCHAR, wordID BIGINT)")
                #sqlContext.sql("CREATE TABLE IF NOT EXISTS word_occurrences(word VARCHAR, wordID BIGINT, documentID BIGINT, occurrences INTEGER)")
                
                dictionary_schema = StructType(\
                    [StructField("word", StringType(), True)])
                word_occurrence_schema = StructType(\
                        [StructField("word", StringType(), True), \
                        StructField("documentID", LongType(), True), \
                        StructField("occurrences", IntegerType(), True)])
                # TODO: column of word_occcurrence_schema
                #[StructField("wordID", LongType(), True), \
                
                test_schema = StructType(\
			[StructField("word", StringType(), True), \
			 StructField("occurrences", StringType(), True)])
                
		invertedIndexStrings = self.invertedIndex.map(lambda kv_pair: (kv_pair[0], str(kv_pair[1])))
                test_df = sqlContext.createDataFrame(invertedIndexStrings, test_schema)
		test_df.write.jdbc(url=url, table="index_test", mode="overwrite", properties=properties)
                
                word_occurrence = self.invertedIndex.flatMap(splitTuple)
                print 'word occurrence',  word_occurrence.collect()
                word_occurrence_df = sqlContext.createDataFrame(word_occurrence, word_occurrence_schema)
                word_occurrence_df.write.jdbc(url=url, table="word_occurrences", mode="overwrite", properties=properties)

	        dictionary = self.invertedIndex.map(lambda kv_pair: (kv_pair[0],))
		dictionary_df = sqlContext.createDataFrame(dictionary, dictionary_schema).withColumn("wordID", monotonically_increasing_id())
                print 'dictionary_df', dictionary_df.collect()
                print 'dictionary_df take 1', dictionary_df.take(1)
                dictionary_df.write.jdbc(url=url, table="dictionary", mode="overwrite", properties=properties)


                		
