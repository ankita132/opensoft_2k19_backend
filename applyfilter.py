import re
import pickle
import datetime
from acts_detector_2 import *
from dateutil.parser import parse
from Judgement import *
import os
from query_search import *
from flask import Blueprint, jsonify, abort, request
from urllib.request import urlopen

filtering = Blueprint('foo', __name__)

filenametext = open("doc_path_ttl_id.txt")
filenametext1 = filenametext.readlines()
allfiles = []
for i in filenametext1:
    a = [m.start() for m in re.finditer('-->', i)]
    allfiles.append(i[:a[0]] + ".txt")


@filtering.route('/getData', methods=['POST'])
def get_data():
    data = request.get_json(force=True)

    def is_date(string):
        try:
            parse(string)
            return True
        except ValueError:
            return False

    dicti_new = {}
    dicti_new['from'] = data['from']
    dicti_new['to'] = data['to']
    dicti_new['category'] = data['category']
    dicti_new['acts_sited'] = data['acts_sited']
    dicti_new['judge_name'] = data['judge_name']
    dicti_new['choice'] = data['choice']
    dicti_new['query'] = data['query']

    file = open('keywords.pickle', 'rb')
    data1 = pickle.load(file)
    file.close()

    file = open('acts_inv.pickle', 'rb')
    data2 = pickle.load(file)
    file.close()

    file = open('judgelist.pickle', 'rb')
    data3 = pickle.load(file)
    file.close()

    file = open('case-keywords.pickle', 'rb')
    data4 = pickle.load(file)
    file.close()

    file = open('case-judge.pickle', 'rb')
    data5 = pickle.load(file)
    file.close()

    file = open('case-date.pickle', 'rb')
    data6 = pickle.load(file)
    file.close()

    punctuations = '''!()[]{};:'"\,<>./?@#$%^&*_~'''

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

    def preprocess_judge(case_file):
        i = case_file.lower()
        i = i.replace("hon'ble", " ").replace("mr"," ").replace("justice"," ")
        no_punct = ""
        for char in i:
            if char not in punctuations:
                no_punct = no_punct + char
            else:
                no_punct = no_punct + " "
        i.strip()
        i = re.sub(' +', ' ', no_punct)
        i = i.strip()
        case_file = i
        return case_file


    def applyfil(dicti_new):
        flag = 0
        newlist = set([])
        if dicti_new['judge_name'] == "":
            judgelist = set([])
            flag += 1
        else:
            try:
                n = preprocess_judge(dicti_new['judge_name'])
                judgelist = set(data3[n])
                if len(newlist) == 0:
                    newlist.update(judgelist)
                else:
                    newlist.update(judgelist)
            except:
                return []
        if dicti_new['category'] == "":
            catlist = set([])
            flag += 1
        else:
            try:
                temp_l = [i+".txt" for i in data1[dicti_new['category']]]
                catlist = set(temp_l)
                newlist = newlist.intersection(catlist)
            except:
                return []

        if dicti_new['acts_sited'] == "":
            actlist = set([])
            flag += 1
        else:
            try:
                actlist = set(data2[dicti_new['acts_sited']])
                if len(newlist) == 0 and flag == 2:
                    newlist.update(actlist)
                else:
                    newlist = newlist.intersection(actlist)
            except:
                return []
        # newlist = judgelist.intersection(actlist.intersection(catlist))
        # print(catlist)
        # print(actlist)
        # print(judgelist)

        finallist = []

        if flag == 3 and dicti_new["from"] == "" and dicti_new["to"] == "":
            finallist = allfiles[:20]

        elif flag != 3:
            if dicti_new["from"] == "":
                datefrom = datetime.datetime.now() - datetime.timedelta(days=1000*365)
            else:
                datefrom = datetime.datetime.strptime(
                    dicti_new['from'], '%d-%m-%Y')

            if dicti_new["to"] == "":
                dateto = datetime.datetime.now()
            else:
                dateto = datetime.datetime.strptime(dicti_new['to'], '%d-%m-%Y')

            for j in newlist:
                date = data6[j]
                if date >= datefrom and date <= dateto:
                    finallist.append(j)
                break

        # print(finallist)

        summary = []
        casename = []
        from gensim.summarization.summarizer import summarize
        from gensim.summarization import keywords
        for i in finallist:
            file = urlopen("https://cloud-cube.s3.amazonaws.com/dkt220sxmwoo/public/All_FT/" + i)
            sentences = file.readlines()
            sentences = [k.decode("utf-8") for k in sentences]
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
                    gensummary += summarize("\n".join(sentences),
                                            word_count=100)
                except:
                    gensummary += "\n".join(sentences)[:100]
            summary.append(gensummary)

        # print(summary)
        outlist = []

        for j, i in enumerate(finallist):
            outdict = {}
            outdict['url'] = i
            outdict['casename'] = casename[j]
            outdict['summary'] = summary[j]
            outdict['acts_sited'] = list(getActs("https://cloud-cube.s3.amazonaws.com/dkt220sxmwoo/public/All_FT/" + i))

            try:
                outdict['keywords'] = data4[i[:-4]]
            except:
                outdict['keywords'] = []

            try:
                outdict['judge'] = data5[i]
            except:
                outdict['judge'] = ""
            outdict['judgement'] = find_judgement(i)

            outlist.append(outdict)

        return outlist

    def run(dicti_new):
        if dicti_new['choice'] == "acts" or dicti_new['choice'] == "cases":
            a = getResults(dicti_new['query'], dicti_new['choice'])
        else:
            a = applyfil(dicti_new)
        return a

    a = run(dicti_new)

    return jsonify({'data': a})
