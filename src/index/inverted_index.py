from pyspark import SparkContext
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql.functions import monotonically_increasing_id
import time
import logging
import urllib2
import httplib
import traceback
import html2text
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def addSourceID(word, docID):
	return ((word, docID), 1)

def flattenTuple(t):
	'''Remove nested tuples (((d, f), (d, f)), (d,f )) -> ((d, f), (d, f), (d, f))'''
        while type(t) == tuple and len(t) > 0 and type(t[0]) == tuple and len(t[0]) > 0 and type(t[0][0]) == tuple:
                l = list(t[0])
                for elem in t[1:]:
                        l.append(elem)
                t = tuple(l)
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


def getWebsiteText(url, preprocess):
    # Read from url
    valid_response = False
    attempts = 0
    max_attempts = 5
    while not valid_response:
        try: 
            resp = urllib2.urlopen(url)
            valid_response = True
        except urllib2.HTTPError, e:
            logging.error(url + ': HTTPError = ' + str(e.code))
            if e.code == 404:
                return ""
        except urllib2.URLError, e:
            logging.error(url + ': URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            logging.error(url + ': HTTPException')
        except Exception:
            logging.error(url + ': generic exception: ' + traceback.format_exc())
        attempts += 1
        if attempts >= max_attempts:
            return ""
        time.sleep(1)
    html = resp.read()

    # Convert html to text
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup('script')]
    [s.extract() for s in soup('style')]
    text = soup.get_text(' ')
    words = text.lower().split()
    if preprocess:
        # Stopping
        stop = set(stopwords.words('english'))
        stopped_text = [i for i in words if i not in stop]

        # Stemming
        porter_stemmer = PorterStemmer()
        stemmed_text = [porter_stemmer.stem(i) for i in stopped_text]
        words = stemmed_text 
    
    final_string = ""
    for word in words:
        word = word.replace(u'\00', '')
        # Split hyphenated words
        for w in word.split('-'):
            # Trim punctuation
            alphanum = filter(unicode.isalnum, w)
            final_string += alphanum
            final_string += " "
    return final_string


class InvertedIndex:
	def __init__(self, sc, preprocessWords):
		self.invertedIndex = sc.emptyRDD()
                self.preprocessWords = preprocessWords

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

        def indexTable(self, sqlContext, db_url, table, properties):
            websites_df = sqlContext.read.jdbc(url=db_url, table=table, properties=properties)
            websites_df = websites_df.select("id", "link")
            websites_rdd = websites_df.rdd

            if self.preprocessWords:
                    websites_rdd = websites_rdd.map(lambda r: (r["id"], getWebsiteText(r["link"], True)))
            else:
                    websites_rdd = websites_rdd.map(lambda r: (r["id"], getWebsiteText(r["link"], False)))
            
            websites_rdd = websites_rdd.flatMapValues(lambda text: text.split()) \
                    .map(lambda kv_pair: addSourceID(kv_pair[1], kv_pair[0])) \
                    .reduceByKey(lambda a, b: a+b)

            self.invertedIndex = websites_rdd.map(lambda kv_pair: (kv_pair[0][0], kv_pair[0][1], kv_pair[1])) #\
                    #.reduceByKey(lambda a, b: (a,b)) \
                    #.map(lambda kv_pair: (kv_pair[0], flattenTuple(kv_pair[1])))

	def writeToDatabase(self, sqlContext, url, properties):
                dictionary_schema = StructType(\
                    [StructField("word", StringType(), False)])

                word_occurrence_schema = StructType(\
                        [StructField("word", StringType(), False), \
                        StructField("document_id", LongType(), False), \
                        StructField("occurrences", IntegerType(), True)])

                dictionary = self.invertedIndex.map(lambda kv_pair: (kv_pair[0],)).distinct()
		dictionary_df = sqlContext.createDataFrame(dictionary, dictionary_schema).withColumn("word_id", monotonically_increasing_id())
                dictionary_df.write.jdbc(url=url, table="cs_dictionary_raw", mode="overwrite", properties=properties)

                #word_occurrence = self.invertedIndex.flatMap(splitTuple)
                word_occurrence_df = sqlContext.createDataFrame(self.invertedIndex, word_occurrence_schema)

                sqlContext.registerDataFrameAsTable(dictionary_df, "dict")
                sqlContext.registerDataFrameAsTable(word_occurrence_df, "word_occ")

                # Use word_id column from dictionary
                word_occurrence_with_ids = word_occurrence_df.join(dictionary_df, word_occurrence_df.word == dictionary_df.word) \
                        .select("word_id", "document_id", "occurrences")
                word_occurrence_with_ids.write.jdbc(url=url, table="cs_word_occurrences_raw", mode="overwrite", properties=properties)
