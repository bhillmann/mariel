from scipy.stats import entropy
import numpy as np

def kullback_leibler(pk, qk):
    avg = (entropy(pk, qk) + entropy(qk, pk))/2
    return 1-np.exp(-1*avg)