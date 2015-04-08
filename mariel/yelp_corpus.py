import yelp_preprocess
from gensim import corpora
from yelp_stream import yield_midwest_json
from kaggle_preprocessing import preprocess_pipeline
import os

class YelpCorpus:
    def __init__(self):
        p = os.path.join(os.path.dirname(__file__), 'cache')
        self.d = corpora.Dictionary().load(os.path.join(p, 'yelp_blei.lda-c'))

    def __iter__(self):
        for d in yield_midwest_json():
            yield self.d.doc2bow(preprocess_pipeline(d['text'], "english", "LancasterStemmer", False, True, True))

if __name__ == '__main__':
    corpus = YelpCorpus()
    path = os.path.join(os.path.dirname(__file__), 'cache')
    corpora.BleiCorpus.serialize(os.path.join(path, 'yelp_blei.lda-c'), corpus)