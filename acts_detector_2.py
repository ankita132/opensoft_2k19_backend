import pygtrie
import re

my_trie = pygtrie.StringTrie()

actsfile = open("actlist.txt")
actslist = actsfile.readlines()
punctuations = '''!()[]{};:'"\,<>./?@#$%^&*_~'''

processed_actslist = []


def preprocess(case_file):
    i = case_file.lower()
    i = i.replace("-", " ")
    i = re.sub("[\(\[].*?[\)\]]", "", i)
    no_punct = ""
    for char in i:
        if char not in punctuations:
            no_punct = no_punct + char
    i.strip()
    i = re.sub(' +', ' ', no_punct)
    case_file = i
    return case_file


for j, i in enumerate(actslist):
    i = preprocess(i)
    i = i[:-1]
    processed_actslist.append(i)
    my_trie[i.replace(" ", "/")] = j

dicti = {}
for j, i in enumerate(processed_actslist):
    key = i[:-5]
    if key in dicti.keys():
        try:
            if dicti[key][0] < int(i[-4:]):
                dicti[i[:-5]] = [int(i[-4:]), j]
        except:
            #print(j , " : ", i)
            pass

    else:
        try:
            dicti[i[:-5]] = [int(i[-4:]), j]
        except:
            #print(j , " : ", i)
            pass

year_disambiguated = list(dicti.keys())
for i in year_disambiguated:
    my_trie[i.replace(" ", "/")] = dicti[i]


def getActs(filestr):
    actlist_ = []
    case_file = open(filestr)
    case_file = case_file.read()

    listi = [0]
    listi.extend([m.start() + 1 for m in re.finditer(' ', case_file)])
    for i in listi:
        searchstr = preprocess(case_file[i:]).replace(" ", "/")
        #print(str(i) + " : "+ searchstr)
        if my_trie.longest_prefix(searchstr):
            x = my_trie.longest_prefix(searchstr).key.replace("/", " ")
            z = my_trie.longest_prefix(searchstr).value
            try:

                y = int(x[-4:])
                #print( i , " : ",x, " - ", z)
                actlist_.append(x)
            except:
                #print( i , " : ",x ,str(z[0]), "- ",str(z[1]))
                actlist_.append(str(x) + " " + str(z[0]))

    return set(actlist_)
