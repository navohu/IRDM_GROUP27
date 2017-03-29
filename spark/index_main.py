from pyspark import SparkContext, SQLContext
from simple_index import InvertedIndex
from properties import properties, db_url

import sys

reload(sys)
sys.setdefaultencoding('utf8')

sc = SparkContext()
sqlContext = SQLContext(sc)
index = InvertedIndex(sc)

index.indexTable(sqlContext, db_url, "cs_sites", properties)

index.writeToDatabase(sqlContext, db_url, properties)

