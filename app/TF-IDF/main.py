from sklearn.feature_extraction.text import TfidfVectorizer
import math

document_0 = "China has a strong economy that is growing at a rapid pace. However politically it differs greatly from the US Economy."
document_1 = "At last, China seems serious about confronting an endemic problem: domestic violence and corruption."
document_2 = "Japan's prime minister, Shinzo Abe, is working towards healing the economic turmoil in his own country for his view on the future of his people."
document_3 = "Vladimir Putin is working hard to fix the economy in Russia as the Ruble has tumbled."
document_4 = "What's the future of Abenomics? We asked Shinzo Abe for his views"
document_5 = "Obama has eased sanctions on Cuba while accelerating those against the Russian Economy, even as the Ruble's value falls almost daily."
document_6 = "Vladimir Putin is riding a horse while hunting deer. Vladimir Putin always seems so serious about things - even riding horses. Is he crazy?"

all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]

def cosine_similarity(vector1, vector2):
	dot_product = sum(p*q for p,q in zip(vector1, vector2))
	magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
	if not magnitude:
		return 0
	return dot_product/magnitude

def TF_IDF(corpus):
	tokenize = lambda doc: doc.lower().split(" ")
	vectorizer = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
	return vectorizer.fit_transform(corpus)

def get_comparisons(tfidf):
	results = []
	for count_0, doc_0 in enumerate(tfidf.toarray()):
		for count_1, doc_1 in enumerate(tfidf.toarray()):
			if count_1 <= count_0:
				continue
			else:
				results.append((cosine_similarity(doc_0, doc_1), count_0, count_1))
	return results


def main():
	tfidf = TF_IDF(all_documents)
	results = get_comparisons(tfidf)

	print("(Cosine Similarity, Document 1, Document 2)")
	for x in sorted(results, reverse = True):
		print x


if __name__ == '__main__':
	main()