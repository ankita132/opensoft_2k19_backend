import re
import pygtrie
from urllib.request import urlopen

cases_list = open("doc_path_ttl_id.txt")
cases_list = cases_list.readlines()


my_trie = pygtrie.StringTrie()

dic = {}

for i in cases_list:
	a = [m.start() for m in re.finditer('-->', i)]
	a[1] = a[1]  + 3
	my_trie[i[a[1]:][:-1].replace(" ","/")] = i[:a[0]] 


def getCases(filename):
	case_file = urlopen(filename)
	case_file = case_file.read().decode("utf-8")
	listi = [0]
	listi.extend([m.start() + 1 for m in re.finditer(' ', case_file)])

	outlist = []
	for i in listi:
	    outdict = {}
	    searchstr = case_file[i:].replace(" ","/")
	    if my_trie.longest_prefix(searchstr):
	        x = my_trie.longest_prefix(searchstr).key.replace("/"," ")
	        z = my_trie.longest_prefix(searchstr).value
	        #print( i , " : ",x, " --> ", z)
	        outdict['index1'] = i
	        outdict['index2'] = i + len(z)
	        outdict['url'] = "https://cloud-cube.s3.amazonaws.com/dkt220sxmwoo/public/All_FT/" + z + ".txt"
	        outlist.append(outdict)
	return outlist


# filestr = "All_FT/1980_D_41.txt"
# print(getCases(filestr))