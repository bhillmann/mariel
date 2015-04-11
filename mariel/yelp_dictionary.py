from yelp_stream import yield_midwest_json
from kaggle_preprocessing import preprocess_pipeline
from gensim import corpora
import os
from read_subjectivity_clues import Codeword

if __name__ == '__main__':
    codeword = Codeword()
    d_final = corpora.Dictionary(
        preprocess_pipeline(d['text'], codeword, "english", "LancasterStemmer", False, True, True) for d in
        yield_midwest_json()
    )
    once_ids = [tokenid for tokenid, docfreq in d_final.dfs.items() if docfreq <= 4]
    d_final.filter_tokens(once_ids)
    d_final.compactify()
    path = os.path.join(os.path.dirname(__file__), 'cache')
    d_final.save(os.path.join(path, 'yelp_blei.dict'))
    with open(os.path.join(path, 'token2id.dat'), 'w') as f:
        for key in range(len(d_final.keys())):
            f.write(d_final[key] + "\n")
