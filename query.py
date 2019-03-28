from invdx import build_data_structures, InvertedIndex, DocumentLengthTable
from rank import score_BM25
import operator
import pickle


class QueryProcessor:
	def __init__(self, queries, idx, dlt):
	# def __init__(self, queries, corpus):
		self.queries = queries
		self.index=idx
		self.dlt=dlt
		# print(dlt[])

	def run(self, filtered_doc_list):
		results = []
		for query in self.queries:
			results.append(self.run_query(query,filtered_doc_list))
		return results

	def run_query(self, query,filtered_doc_list):
		'''
		Run the BM25 Algorithm on all the terms in the query over all the filtered documents. 
		The score of all the filtered documents in updated.
		Finally a descending order of the filtered documents is obtained. 
		'''
		query_result = dict()
		for term in query:
			if term in self.index:
				doc_dict_original = self.index[term] # retrieve index entry
				# filtered=list()
				doc_dict = {k: v for k, v in doc_dict_original.items() if k in filtered_doc_list}
				for docid, freq in doc_dict.items(): #for each document and its word frequency
					
					score = score_BM25(n=len(doc_dict), f=freq, qf=1, r=0, N=len(self.dlt),
									   dl=self.dlt.get_length(docid), avdl=self.dlt.get_average_length()) # calculate score
					if docid in query_result: #this document has already been scored once
						query_result[docid] += score
					else:
						query_result[docid] = score
		return query_result