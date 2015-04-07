from yelp_stream import yield_midwest_json
from kaggle_preprocessing import preprocess_pipeline
from gensim import corpora

if __name__ == '__main__':
    d_final = corpora.Dictionary(
        preprocess_pipeline(d['text'], "english", "LancasterStemmer", False, True, True) for d in
        yield_midwest_json()
    )
    once_ids = [tokenid for tokenid, docfreq in d_final.dfs.items() if docfreq == 1]
    d_final.filter_tokens(once_ids)
    d_final.compactify()
    d_final.save('cache/yelp_blei.dict')