from gensim import corpora, models, similarities

dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))