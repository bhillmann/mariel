from scipy.stats import entropy

def kullback_leibler(pk, qk):
    return (entropy(pk, qk) + entropy(qk, pk))/2