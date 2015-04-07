from gensim import models
from gensim import corpora

if __name__ == "__main__":
    corpora_path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/midwest.dict'
    d = corpora.Dictionary.load(corpora_path)

    corpus_path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/midwest.mm'
    corpus = corpora.MmCorpus(corpus_path)

    lda = models.LdaModel(corpus, id2word=d, num_topics=40, passes=20)
    lda.save('C:/Users/Benjamin/Projects/mariel/mariel/cache/midwest.lda')

    print(corpus)
