setwd("C:/Users/Benjamin/Projects/mariel/R")
library("lda")
library("ggplot2")
library("LDAvis")
library("servr")

yelp.documents = read.documents("../mariel/cache/yelp_blei.lda-c")
term.frequency = word.counts(yelp.documents)
yelp.documents = filter.words(yelp.documents,
                        as.numeric(names(term.frequency)[term.frequency <= 4]))
boolean = sapply(yelp.documents, function(x) {sum(x) > 0})
yelp.documents = yelp.documents[boolean]
term.frequency = word.counts(yelp.documents)
term.frequency = term.frequency[term.frequency > 4]
yelp.ratings = read.csv("../mariel/cache/star_vector.csv")
yelp.ratings = yelp.ratings[2]$X1
yelp.ratings = as.numeric(yelp.ratings[boolean])
yelp.ratings[is.na(yelp.ratings)] = 0

K = 20
params = sample(c(-1,1), K, replace=TRUE)

token2id = read.table('C:/Users/Benjamin/Projects/mariel/mariel/cache/token2id.dat', header=FALSE)
yelp.vocab = token2id$V1

# Compute some statistics related to the data set:
D <- length(yelp.documents)  # number of documents (2,000)
W <- length(yelp.vocab)  # number of terms in the vocab (14,568)
doc.length <- sapply(yelp.documents, function(x) sum(x[2, ]))  # number of tokens per document [312, 288, 170, 436, 291, ...]
N <- sum(doc.length)  # total number of tokens in the data (546,827)
term.frequency <- as.integer(word.counts(yelp.documents, vocab=yelp.vocab))  # frequencies of terms in the corpus [8939, 5544, 2411, 2410, 2143, ...]

alpha = 1.25
eta = 0.02
t1 <- Sys.time()

result = slda.em(documents=yelp.documents,
                                     K=K,
                                     vocab=yelp.vocab,
                                     num.e.iterations=10,
                                     num.m.iterations=4,
                                     alpha=alpha, eta=eta,
                                     yelp.ratings,
                                     params,
                                     variance=0.25,
                                     lambda=1.0,
                                     logistic=FALSE,
                                     method="sLDA")

t2 <- Sys.time()
t2 - t1  # about 24 minutes on laptop

Topics <- apply(top.topic.words(result$topics, 5, by.score=TRUE),
                                 2, paste, collapse=" ")

coefs <- data.frame(coef(summary(result$model)))

theme_set(theme_bw())

coefs <- cbind(coefs, Topics=factor(Topics, Topics[order(coefs$Estimate)]))

coefs <- coefs[order(coefs$Estimate),]

qplot(Topics, Estimate, colour=Estimate, size=abs(t.value), data=coefs) +
     geom_errorbar(width=0.5, aes(ymin=Estimate-Std..Error,
                                                      ymax=Estimate+Std..Error)) + coord_flip()

theta <- t(apply(result$document_sums + alpha, 2, function(x) x/sum(x)))
phi <- t(apply(t(result$topics) + eta, 2, function(x) x/sum(x)))

YelpReviews <- list(phi = phi,
                     theta = theta,
                     doc.length = doc.length,
                     vocab = yelp.vocab,
                     term.frequency = term.frequency)

# create the JSON object to feed the visualization:
json <- createJSON(YelpReviews$phi, YelpReviews$theta, YelpReviews$doc.length, YelpReviews$vocab, YelpReviews$term.frequency)

serVis(json, out.dir = 'vis', open.browser = TRUE)
