import string
import nltk
import re
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# init stemmer
porter_stemmer=PorterStemmer()

# init lemmatizer
lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words('english'))

translator = str.maketrans('', '', string.punctuation)

def scrub_words(text):
    """Basic cleaning of texts."""
    
    # remove html markup
    text=re.sub("(<.*?>)","",text)
    
    #remove non-ascii and digits
    text=re.sub("(\\W|\\d)"," ",text)
    
    #remove whitespace
    text=text.strip()
    return text

def process_query(s):
	"""Remove stopwords, punctuations and numbers before query expansion"""
	s=s.lower()

	s_new = re.sub(r'\d+','',s)
	no_punct_s=s_new.translate(translator)

	
	tokens = word_tokenize(no_punct_s)

	scrubbed_tokens=[scrub_words(w) for w in tokens]
	cleaned_tokens=[i for i in scrubbed_tokens if not i in stop_words]

	processed_text=' '.join(cleaned_tokens)
	return processed_text

def pre_process(s):
	'''
	Remove the punctuations, numbers, stopwords, capitalisation
	Tokenise, stem and lemmatize the query
	'''
	s=s.lower()

	s_new = re.sub(r'\d+','',s)
	no_punct_s=s_new.translate(translator)

	
	tokens = word_tokenize(no_punct_s)

	scrubbed_tokens=[scrub_words(w) for w in tokens]
	cleaned_tokens=[i for i in scrubbed_tokens if not i in stop_words]

	stemmed_tokens=[porter_stemmer.stem(word=word) for word in cleaned_tokens]
	lemmatized_tokens=[lemmatizer.lemmatize(word=word) for word in stemmed_tokens]

	processed_text=' '.join(lemmatized_tokens)
	return processed_text

