import re
import pickle

from acts_detector_2 import *

cases_list = open("subject_keywords.txt")
cases_list = cases_list.readlines()
dicti = {}
for j,i in enumerate(cases_list):
	a = [m.start() for m in re.finditer('-->', i)]
	b = i.find('$$$')
	case = i[:a[0]]
	keywords_list = i[a[1] + 4 : b].split(";")
	
	for k in keywords_list:
		if k in dicti.keys():
			dicti[k].append(case)

		else:
			dicti[k] = [case]

pickle_out = open("keywords.pickle","wb")
pickle.dump(dicti, pickle_out)
pickle_out.close()


from os import listdir
folder = listdir("./All_FT")

dictj = {}

for j,name in enumerate(folder[:2]):
	if(j%500) == 0:
		print(j)
	filestr = "All_FT/" + name
	x = getActs(filestr)
	for i in x:
		if i in dictj.keys():
			dictj[i].append(name)
		else:
			dictj[i] = [name]

pickle_out1 = open("acts_inv.pickle","wb")
pickle.dump(dictj, pickle_out1)
pickle_out1.close()