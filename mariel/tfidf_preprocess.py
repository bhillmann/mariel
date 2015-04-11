from gensim import models
from gensim import corpora
import pandas as pd
import os

def reset_dict_to_tfidf():
    path = os.path.join(os.path.dirname(__file__), 'cache')
    c = corpora.BleiCorpus(os.path.join(path, 'yelp_blei.lda-c'))
    tfidf = models.TfidfModel(c)
    vocab_size = len(tfidf.idfs)
    weights = tfidf[zip(c.id2word.keys(), [1]*vocab_size)]
    df_weights = pd.DataFrame(weights, columns=["id", "weight"])
    df_weights = df_weights.sort('weight', ascending=False)
    df_ids = df_weights['id'][5000:]
    d = corpora.Dictionary().load(os.path.join(path, 'yelp_blei.dict'))
    d.filter_tokens(df_ids.values)
    d.compactify()
    d.save(os.path.join(path, 'yelp_blei.dict'))
    with open(os.path.join(path, 'token2id.dat'), 'w') as f:
        for key in range(len(d.keys())):
            f.write(d[key] + "\n")


if __name__ == "__main__":
    reset_dict_to_tfidf()
