import yelp_preprocess
from gensim import corpora
from yelp_stream import yield_first

class YelpCorpus:
    def __init__(self):
        self.d = corpora.Dictionary().load('cache/real.dict')

    def __iter__(self):
        for d in yield_first():
            yield self.d.doc2bow(yelp_preprocess.preprocess_line(d['text']))

if __name__ == '__main__':
    corpus = YelpCorpus()
    path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/corpus.lda-c'
    corpora.BleiCorpus.serialize(path, corpus)