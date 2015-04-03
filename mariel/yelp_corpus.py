from gensim import corpora
from yelp_stream import yield_file_names

def test_pipeline():
    gen = yield_file_names()
    for i, d in enumerate(gen):
        if i < 100000:
            if i % 1000 == 0:
                print(i)
            yield d
        else:
            break

class YelpCorpus:
    def __init__(self):
        self.d = corpora.Dictionary().load_from_text('cache/real.dict')
        print("hi")

    def __iter__(self):
        for line in open('mycorpus.txt'):
            yield self.d.doc2bow(line.lower().split())

y_c = YelpCorpus()
