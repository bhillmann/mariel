from gensim import corpora
from kaggle_preprocessing import preprocess_pipeline
import os

if __name__ == "__main__":
    p = os.path.join(os.path.dirname(__file__), 'cache')
    d = corpora.Dictionary().load(os.path.join(p, 'yelp_blei.dict'))
    print(d.doc2bow(preprocess_pipeline(
                "I enjoy Cafe Mac's zesty burgers but sometimes I distate their unorthodox pizza.",
                3, "english", "LancasterStemmer", False, True, True)))
    corpus = corpora.BleiCorpus(os.path.join(p, 'yelp_blei.lda-c'))
