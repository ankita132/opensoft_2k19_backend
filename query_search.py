import pickle
from Judgement import *
from acts_detector_2 import *
import re
punctuations = '''!()[]{};:'"\,<>./?@#$%^&*_~'''


def preprocess(case_file):
    i = case_file.lower()
    i = i.replace("-", " ")
    no_punct = ""
    for char in i:
        if char not in punctuations:
            no_punct = no_punct + char
    i.strip()
    i = re.sub(' +', ' ', no_punct)
    case_file = i
    return case_file


actsfile = open("actlist.txt")
actslist1 = actsfile.readlines()
actslist = [preprocess(i) for i in actslist1]
unique_words_acts = set([])
for i in actslist:
    for j in i.split():
        unique_words_acts.add(j)

casesfile = open("doc_path_ttl_id.txt")
cases_list = casesfile.readlines()
caseslist1 = []
casesnum = []
for i in cases_list:
    a = [m.start() for m in re.finditer('-->', i)]
    a[0] = a[0] + 3
    caseslist1.append(i[a[0]: a[1]])
    casesnum.append(i[:a[0]])
caseslist = [preprocess(i) for i in caseslist1]
unique_words_cases = set([])
for i in caseslist:
    for j in i.split():
        unique_words_cases.add(j)


def edit_distance(s1, s2):
    m = len(s1)+1
    n = len(s2)+1
    tbl = {}
    for i in range(m):
        tbl[i, 0] = i
    for j in range(n):
        tbl[0, j] = j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i, j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)
    return tbl[i, j]


def correction(input_word, words_dict):
    minm = 1000
    word = input_word
    for i in words_dict:
        d = edit_distance(input_word, i)
        if(d < minm):
            minm = d
            word = i
    return word


def correct_query(query, mode):
    query = preprocess(query)
    new_query = ""
    for i in query.split():
        if mode == "acts":
            new_query += correction(i, unique_words_acts) + " "
        if mode == "cases":
            new_query += correction(i, unique_words_cases) + " "
    return new_query


def test_tfidf(query, mode):
    retlist = []
    query = correct_query(query, mode)
    maxscore = 0
    scorelist = []
    retlist = []
    if(mode == "acts"):
        l = actslist
        m = actslist1
    elif(mode == "cases"):
        l = caseslist
        m = caseslist1

    for i, act in enumerate(l):
        score = 0
        l = act.split()
        for words in query.split():
            if words in act:
                score += 1
        scorelist.append((i, score))
        if score > maxscore:
            maxscore = score

    scores = sorted(scorelist, key=lambda x: -x[1])
    for i in scores:
        if i[1] == maxscore:
            if mode == "acts":
                retlist.append(m[i[0]][:-1])
            else:
                retlist.append(casesnum[i[0]])
    return retlist


file = open('act-path.pickle', 'rb')
data1 = pickle.load(file)
file.close()

file = open('case-keywords.pickle', 'rb')
data4 = pickle.load(file)
file.close()

file = open('case-judge.pickle', 'rb')
data5 = pickle.load(file)
file.close()


def generateSummary_act(file):
    f = open(file)
    sentences = f.readlines()
    return sentences[0]


def generate_case(finallist):
    summary = []
    casename = []
    from gensim.summarization.summarizer import summarize
    from gensim.summarization import keywords
    for i in finallist:
        file = open("All_FT/" + i[:-3] + ".txt")
        sentences = file.readlines()
        line = 0
        while sentences[line] == "":
            line += 1
        casename.append(sentences[line])
        k = 0
        for j, i in enumerate(sentences):
            if i[:2] == "1.":
                k = j
                break
        sentences = sentences[k:]
        sentences = [" ".join(i.split()[1:]) for i in sentences]
        prefix = "\n".join(sentences[:-2])
        postfix = "\n".join(sentences[-2:])

        gensummary = ""
        try:
            gensummary += summarize(prefix, word_count=100)
            gensummary += summarize(postfix, word_count=100)
        except:
            try:
                gensummary += summarize("\n".join(sentences), word_count=100)
            except:
                gensummary += "\n".join(sentences)[:100]
        summary.append(gensummary)
    # print(summary)
    outlist = []

    for j, i in enumerate(finallist):
        outdict = {}
        outdict['url'] = i[:-3]+".txt"
        outdict['casename'] = casename[j]
        outdict['acts_sited'] = list(getActs("All_FT/" + i[:-3] + ".txt"))
        try:
            outdict['keywords'] = data4[i[:-3]]
        except:
            outdict['keywords'] = []
        try:
            outdict['judge'] = data5[i[:-3]+".txt"]
        except:
            outdict['judge'] = ""

        outdict['summary'] = summary[j]
        outdict['judgement'] = find_judgement(i[:-3]+".txt")
        outlist.append(outdict)
    return outlist


def getResults(query, mode):
    finallist = test_tfidf(query, mode)
    if mode == "acts":
        outlist = []
        for j, i in enumerate(finallist):
            outdict = {}
            try:
                outdict['url'] = data1[i]
                outdict['casename'] = i
                outdict['summary'] = generateSummary_act(data1[i])
            except:
                outdict['url'] = ""
                outdict['casename'] = i
                outdict['summary'] = "No data exists"

            outlist.append(outdict)
        return outlist
    else:
        return generate_case(finallist)

# print(getResults("aadhar","acts"))
