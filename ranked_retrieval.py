import pickle
from parse import *
from query import QueryProcessor
import operator
from invdx import build_data_structures, InvertedIndex, DocumentLengthTable
from pre_process import *
from urllib.request import urlopen

from urllib.request import urlopen, ProxyHandler, build_opener, install_opener

#Load the pre-trained word embeddings
from gensim.models.keyedvectors import KeyedVectors
from gensim.models import FastText

#embed_model = FastText.load_fasttext_format('cc.en.300.bin')

#Load the already generated inverted index
file = urlopen("https://cloud-cube.s3.amazonaws.com/dkt220sxmwoo/public/inv_index.pkl")
idx = pickle.load(file)
file.close()

#load the generated document length inverted index
file = urlopen("https://cloud-cube.s3.amazonaws.com/dkt220sxmwoo/public/doc_length.pkl")
dlt = pickle.load(file)
file.close()

def query_expansion(q0,k=3):
	'''
	The function to expand the query with the help of word embeddings
	Input: q0 : The query which needs to be expanded
			k : The number of similar tokens we want to add for each token in the query(defaults to 3)

	Output: An expanded query obtained by appending similar terms(with similar embeddings) for each token in the original query
	'''
	qe = []
	q0=process_query(q0)			#removes the stop words and punctuations from the query
	for word in q0.split(' '): 
		expanded_words=[]
		try:
			all_pairs=embed_model.most_similar(word)[:k]		#loadinig the top k similar words for the token
			expanded_words = [pair[0] for pair in all_pairs]
			expanded_words.append(word)
		except:
			expanded_words.append(word)		
		qe.extend(expanded_words)
	
	qe=list(set(qe))
	qe=' '.join(qe)				#expanded query appending all the similar terms
	return qe

def ranked_retrieval(query, list_of_filtered_docs):
	'''
	Function to retrieve the ranked documents based on the BM25 algorithm
	INput :	query: The query for which we want to retrieve the documents
			list_of_filtered_docs: THe filtered documents that we want to rank.(obtained on applying all the filters)

	Output: The list of ranked documents based on the BM25 score.
	'''

	#expand the original query using word embeddings
	#query=query_expansion(query)				

	#pre-processing the query - stemming and lemmatization
	queries=[pre_process(query).rstrip().split()]
	proc = QueryProcessor(queries, idx, dlt)
	results = proc.run(list_of_filtered_docs)
	
	result=results[0]
	sorted_x = sorted(result.items(), key=operator.itemgetter(1))
	sorted_x.reverse()
	index = 0
	final_ranked_docs=[]
	for i in sorted_x[:100]:
		tmp = (i[0], index, i[1])
		final_ranked_docs.append(i[0])
		index += 1
	return final_ranked_docs

# def main():
# 	# qp = QueryParser(filename='../text/queries.txt')

# 	# qp.parse()
# 	# queries = qp.get_queries()
# 	########queries is a list of queries
# 	q="what is income tax? i want to know"
# 	# q=query_expansion(q)
# 	# queries=[pre_process(q).rstrip().split()]
# 	# print(queries)

# 	print("Started")

# 	# cp = CorpusParser(filename='../text/corpus.txt')
# 	# cp.parse()
# 	# corpus = cp.get_corpus()
# 	# ##corpus is a dictionary with the doc id as key and text as value
# 	# proc = QueryProcessor(queries, corpus)
	
# 	# inv_index_file="../inv_index.pkl"
# 	# doc_lenth_file="../doc_length.pkl"

# 	# proc = QueryProcessor(queries, inv_index_file, doc_lenth_file)
# 	# print("Built the dictionary")
	
# 	# filtered_doc_list=proc.doc_list
# 	filtered_doc_list=['2000_H_88','1967_L_8','2009_R_134','1964_L_8']

# 	ranked_retrieval(q,filtered_doc_list)

# 	# results = proc.run(filtered_doc_list)
	
# 	# qid = 0
# 	# for result in results:
# 	# 	sorted_x = sorted(result.items(), key=operator.itemgetter(1))
# 	# 	sorted_x.reverse()
# 	# 	index = 0
# 	# 	for i in sorted_x[:100]:
# 	# 		tmp = (qid, i[0], index, i[1])
# 	# 		print ('{:>1}\tQ0\t{:>4}\t{:>2}\t{:>12}\tNH-BM25'.format(*tmp))
# 	# 		index += 1
# 	# 	qid += 1


# if __name__ == '__main__':
# 	main()
