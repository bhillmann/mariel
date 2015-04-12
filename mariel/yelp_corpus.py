import yelp_preprocess
from gensim import corpora
from yelp_stream import yield_midwest_json
from kaggle_preprocessing import preprocess_pipeline
from read_subjectivity_clues import Codeword
import os

class YelpCorpus:
    def __init__(self):
        p = os.path.join(os.path.dirname(__file__), 'cache')
        self.codeword = Codeword()
        self.d = corpora.Dictionary().load(os.path.join(p, 'yelp_blei.dict'))

    def __iter__(self):
        i = 0
        if i == 0:
            i = 1
            yield self.d.doc2bow(preprocess_pipeline(
                "I enjoy Cafe Mac's zesty burgers but sometimes I distate their unorthodox pizza.",
                3, "english", "LancasterStemmer", False, True, True))
        else:
            for d in yield_midwest_json():
                yield self.d.doc2bow(preprocess_pipeline(d['text'], d['stars'], "english", "LancasterStemmer", False, True, True))

if __name__ == '__main__':
    corpus = YelpCorpus()
    path = os.path.join(os.path.dirname(__file__), 'cache')
    corpora.BleiCorpus.serialize(os.path.join(path, 'yelp_blei.lda-c'), corpus)