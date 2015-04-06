from gensim import models
from gensim import corpora

if __name__ == "__main__":
    corpora_path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/real.dict'
    d = corpora.Dictionary.load(corpora_path)

    corpus_path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/corpus.mm'
    corpus = corpora.MmCorpus(corpus_path)

    lda = models.LdaModel(corpus, id2word=d, num_topics=20, passes=20)
    lda.save('C:/Users/Benjamin/Projects/mariel/mariel/cache/yelp.lda')

    print(corpus)
