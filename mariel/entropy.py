from scipy.stats import entropy

def kullback(pk, qk):
    return (entropy(pk, qk) + entropy(qk, pk))/2