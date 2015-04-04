from gensim.models.ldamulticore import LdaMulticore
from gensim import corpora

corpora_path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/real.dict'
d = corpora.Dictionary.load(corpora_path)

corpus_path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/corpus.lda-c'
corpus = corpora.BleiCorpus.load(corpus_path)

print(corpus)
