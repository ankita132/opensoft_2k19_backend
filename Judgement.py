from os.path import isfile, join
from os import listdir
import glob
import os
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import string
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import re
from nltk.corpus import stopwords
# nltk.download('stopwords')
# nltk.download('wordnet')

path = "https://drive.google.com/open?id=1ROglsQKBaUkcjQ7N7oboB5m3RBFwGXkq"
filenames = os.listdir(path)
documents = []


def f(sentences):
    k = 0
    for j, i in enumerate(sentences):
        if i[:2] == "1.":
            k = j
            break
    sentences = sentences[k:]
    return sentences


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


i = 0
for filename in filenames:
    if(i > 1000):
        break
    i = i+1
    file = open(path+'/'+filename)
    s = file.readlines()
    s = f(s)
    documents.append(s[-1])
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)
true_k = 4
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()


def kmeans(sent):
    X = vectorizer.transform(sent)
    predicted = model.predict(X)
    if predicted[0] == 0:
        return 'Dismissed'
    elif predicted[0] == 1:
        return 'Allowed'
    elif predicted[0] == 2:
        return 'Disposed Of'
    elif predicted[0] == 3:
        return 'Order Accordingly'


def fun2find(sent):
    word1 = ''
    if 'appeal' in sent:
        word1 = 'Appeal '
    elif 'petit' in sent:
        word1 = 'Petition '

    word2 = ''
    if 'partli' in sent:
        word2 = 'partly '

    flagall = 0
    if 'allow' in sent:
        flagall = 1

    flagdismiss = 0
    if 'dismiss' in sent:
        flagdismiss = 1

    flagdispos = 0
    if 'dispos' in sent:
        flagdispos = 1

    if not (flagall and flagdismiss and flagdispos):
        if 'order' in sent and 'accordingli' in sent:
            return 'Order Accordingly'

    if flagall+flagdismiss+flagdispos > 1:
        return word1+word2+kmeans(sent)

    judgment = ''
    if flagall:
        judgment = word1+word2+'Allowed'
    elif flagdismiss:
        judgment = word1+word2+'Dismissed'
    elif flagdispos:
        judgment = word1+word2+'Disposed of'

    return judgment


# In[112]:


def find_judgement(filename):
    file = open(path+'/'+filename)
    sentences = file.readlines()
    sentences = f(sentences)
    doc = []
    for sentence in sentences:
        sentence = preprocess(sentence)

        stemmer = PorterStemmer()
        tokens = word_tokenize(sentence)
        stop_words = set(stopwords.words("english"))
        result = [i for i in tokens if not i in stop_words]
        resultstem = []
        for word in result:
            resultstem.append(stemmer.stem(word))
#         lemmatizer=WordNetLemmatizer()
#         resultlem=[]
#         for word in result:
#             resultlem.append(lemmatizer.lemmatize(word))

        doc.append(resultstem)
    # print(sentences[-1].replace('\n',''))
    final = fun2find(doc[-1])
    return final
