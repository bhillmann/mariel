from gensim import corpora
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from read_subjectivity_clues import Codeword

codeword = Codeword()

def build_dictionary(tokens):
    dictionary = corpora.Dictionary([tokens])
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(once_ids)
    dictionary.compactify()
    return dictionary

def strip_line(line):
    sentence = line.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(sentence)
    filtered_words = filter(lambda token: token not in stopwords.words('english'), tokens)
    return " ".join(filtered_words)

def stem(tokens):
    wnl = WordNetLemmatizer()
    return [wnl.lemmatize(token) for token in tokens]

def tokenize(line):
    return nltk.word_tokenize(line)

def preprocess_line(line):
    line = strip_line(line)
    tokens = tokenize(line)
    tokens = tokens + codeword.get_codeword_tokens(tokens)
    return stem(tokens)

