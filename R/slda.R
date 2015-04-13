setwd("C:/Users/Benjamin/Projects/mariel/R")
library("lda")
library("ggplot2")
library("LDAvis")
library("servr")

yelp.documents = read.documents("../mariel/cache/yelp_blei.lda-c")
yelp.documents = filter.words(yelp.documents,
                        as.numeric(names(term.frequency)[term.frequency <= 4]))
boolean = sapply(yelp.documents, function(x) {sum(x) > 0})
yelp.documents = yelp.documents[boolean]
term.frequency = word.counts(yelp.documents)
yelp.ratings = read.csv("../mariel/cache/star_vector.csv")
yelp.ratings = yelp.ratings$X3 - 3
yelp.ratings = as.numeric(yelp.ratings[boolean])
yelp.ratings = yelp.ratings[boolean]
yelp.ratings[is.na(yelp.ratings)] = 1

K = 20
params = seq(-1,1, length.out = K)

token2id = read.table('C:/Users/Benjamin/Projects/mariel/mariel/cache/token2id.dat', header=FALSE)
yelp.vocab = token2id$V1

# Compute some statistics related to the data set:
D <- length(yelp.documents)
W <- length(yelp.vocab)
doc.length <- sapply(yelp.documents, function(x) sum(x[2, ]))
N <- sum(doc.length)
term.frequency <- as.integer(word.counts(yelp.documents, vocab=yelp.vocab))

alpha = 1.0
eta = 1/K
t1 <- Sys.time()

result = slda.em(documents=yelp.documents,
                                     K=K,
                                     vocab=yelp.vocab,
                                     num.e.iterations=20,
                                     num.m.iterations=10,
                                     alpha=alpha, eta=eta,
                                     yelp.ratings,
                                     params,
                                     variance=1,
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

# Write theta and phi
write.csv(file="../mariel/cache/theta.csv", x=theta)
write.csv(file="../mariel/cache/phi.csv", x=phi)
write.csv(file="../mariel/cache/coefs.csv", x=coefs)

YelpReviews <- list(phi = phi,
                     theta = theta,
                     doc.length = doc.length,
                     vocab = yelp.vocab,
                     term.frequency = term.frequency)


# create the JSON object to feed the visualization:
json <- createJSON(YelpReviews$phi, YelpReviews$theta, YelpReviews$doc.length, YelpReviews$vocab, YelpReviews$term.frequency)

serVis(json, out.dir = 'vis', open.browser = TRUE, as.gist = FALSE)


