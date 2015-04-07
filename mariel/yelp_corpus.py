import yelp_preprocess
from gensim import corpora
from yelp_stream import yield_midwest_json
from kaggle_preprocessing import preprocess_pipeline

class YelpCorpus:
    def __init__(self):
        self.d = corpora.Dictionary().load('cache/yelp_blei.dict')

    def __iter__(self):
        for d in yield_midwest_json():
            yield self.d.doc2bow(preprocess_pipeline(d['text'], "english", "LancasterStemmer", False, True, True))

if __name__ == '__main__':
    corpus = YelpCorpus()
    path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/yelp_blei.lda-c'
    corpora.BleiCorpus.serialize(path, corpus)