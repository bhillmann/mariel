from yelp_stream import yield_file_names
import yelp_dictionary
from joblib import Parallel, delayed
from gensim import corpora

def test_pipeline():
    gen = yield_file_names()
    for i, d in enumerate(gen):
        # if i < 100000:
        if i % 1000 == 0:
            print(i)
        yield d
        # else:
        #     break

def process_line(d):
    tokens = yelp_dictionary.preprocess_line(d['text'])
    return corpora.Dictionary([tokens])

if __name__ == '__main__':
    # for line in test_pipeline():
    #     print(line)
    dictionaries = Parallel(n_jobs=8)(delayed(process_line)(d) for d in test_pipeline())
    d_final = corpora.Dictionary()
    i = 0
    while len(dictionaries) > 0:
        i += 1
        if i % 100 == 0:
            print(i)
        d = dictionaries.pop()
        d_final.merge_with(d)
    once_ids = [tokenid for tokenid, docfreq in d_final.dfs.items() if docfreq == 1]
    d_final.filter_tokens(once_ids)
    d_final.compactify()
    d_final.save('cache/real.dict')
