from yelp_stream import yield_midwest_json
import yelp_preprocess
from gensim import corpora

if __name__ == '__main__':
    d_final = corpora.Dictionary([yelp_preprocess.preprocess_line(d['text']) for d in yield_midwest_json()])
    once_ids = [tokenid for tokenid, docfreq in d_final.dfs.items() if docfreq == 1]
    d_final.filter_tokens(once_ids)
    d_final.compactify()
    d_final.save('cache/midwest.dict')