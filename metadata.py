# from os import listdir
# import datetime

# from dateutil.parser import parse

# # def is_date(string):
# #     try:
# #         parse(string)
# #         return True
# #     except ValueError:
# #         return False

# # file = open("./All_FT/1980_D_41.txt")
# # x = file.readlines()

# # dicti = {}

# # flag = 0
# # for i in x:
# # 	i = i.strip()
# # 	if flag == 0:
# # 		if i == "":
# # 			continue
# # 		else:
# # 			dicti['title'] = i
# # 			flag = 1
# # 	else:
# # 		if is_date(i):
# # 			dicti['date'] = datetime.datetime.strptime(i, '%d %B %Y')
# # 		if i.find("The Judgment was delivered by :") != -1:
# # 			dicti['judge'] = i.replace("The Judgment was delivered by : ","")
# # print(dicti)

# ######################################## Previous Cases ################################################
# import re
# import pygtrie
# cases_list = open("doc_path_ttl_id.txt")
# cases_list = cases_list.readlines()

# my_trie = pygtrie.StringTrie()
# for i in cases_list:
# 	a = [m.start() for m in re.finditer('-->', i)]
# 	a[1] = a[1]  + 3
# 	my_trie[i[a[1]:][:-1].replace(" ","/")] = i[:a[0]]

# file = open("./All_FT/1980_D_41.txt")
# case_file = file.read()
# listi = [0]
# listi.extend([m.start() + 1 for m in re.finditer(' ', case_file)])
# for i in listi:
#     searchstr = case_file[i:].replace(" ","/")

#     if my_trie.longest_prefix(searchstr):
#         x = my_trie.longest_prefix(searchstr).key.replace("/"," ")
#         z = my_trie.longest_prefix(searchstr).value
#         print( i , " : ",x, " --> ", z)

# ######################################## Acts sited ################################################
# my_trie1 = pygtrie.StringTrie()
# actsfile = open("actlist.txt")
# actslist = actsfile.readlines()
# punctuations = '''!()[]{};:'"\,<>./?@#$%^&*_~'''

# processed_actslist = []
# def preprocess(case_file):
#     i = case_file.lower()
#     i = i.replace("-"," ")
#     i = re.sub("[\(\[].*?[\)\]]", "", i)
#     no_punct = ""
#     for char in i:
#        if char not in punctuations:
#            no_punct = no_punct + char
#     i.strip()
#     i = re.sub(' +', ' ',no_punct)
#     case_file = i
#     return case_file

# for j,i in enumerate(actslist):
#     i = preprocess(i)
#     i = i[:-1]
#     processed_actslist.append(i)
#     my_trie1[i.replace(" ","/")] = j

# dicti = {}
# for j,i in enumerate(processed_actslist):
# 	key = i[:-5]
# 	if key in dicti.keys():
# 		try:
# 			if dicti[key][0] < int(i[-4:]):
# 				dicti[i[:-5]] = [int(i[-4:]),j]
# 		except:
# 			pass
# 	else:
# 		try:
# 			dicti[i[:-5]] = [int(i[-4:]),j]
# 		except:
# 			pass

# year_disambiguated = list(dicti.keys())
# for i in year_disambiguated:
# 	my_trie1[i.replace(" ","/")] = dicti[i]

# case_file = open("All_FT/1980_D_41.txt")
# case_file = case_file.read()

# listi = [0]
# listi.extend([m.start() + 1 for m in re.finditer(' ', case_file)])
# for i in listi:
#     searchstr = preprocess(case_file[i:]).replace(" ","/")
#     if my_trie1.longest_prefix(searchstr):
#         x = my_trie1.longest_prefix(searchstr).key.replace("/"," ")
#         z = my_trie1.longest_prefix(searchstr).value
#         try:
#             y = int(x[-4:])
#             print( i , " : ",x, " - ", z)
#         except:
#             print( i , " : ",x ,str(z[0]), "- ",str(z[1]))

from flask import Blueprint, jsonify, abort, request


mod = Blueprint('foo', __name__)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@mod.route('/')
def get_tasks(methods=['GET']):
    return jsonify({'tasks': tasks})


@mod.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@mod.route('/getData', methods=['POST'])
def get_data():
    data = request.get_json(force=True)
    return jsonify({'data': data})
