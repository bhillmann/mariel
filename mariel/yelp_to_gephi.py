import networkx as nx
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram
from pylab import *
from similarity_metrics import kullback_leibler
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import pairwise_distances
import os
import pandas as pd


def make_heatmap(data):
    pcolor(data)
    colorbar()
    show()


def make_good_heatmap(D):
    data_dist = 1. - D
    np.fill_diagonal(data_dist, 0.)
    data_dist = squareform(data_dist)

    # Compute and plot first dendrogram.
    fig = plt.figure()
    # x-y width height
    ax1 = fig.add_axes([0.09, 0.1, 0.2, 0.6])
    Y = linkage(data_dist, method='complete')
    Z1 = dendrogram(Y, orientation='right',  color_threshold=.7)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Compute and plot second dendrogram.
    ax2 = fig.add_axes([0.3, 0.71, 0.6, 0.2])
    Z2 = dendrogram(Y, color_threshold=.7)
    ax2.set_xticks([])
    ax2.set_yticks([])

    # Compute and plot the heatmap
    axmatrix = fig.add_axes([0.3, 0.1, 0.6, 0.6])
    idx1 = Z1['leaves']
    idx2 = Z2['leaves']
    D = D[idx1,:]
    D = D[:,idx2]
    im = axmatrix.matshow(D, aspect='auto', origin='lower')
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])

    # Plot colorbar.
    axcolor = fig.add_axes([0.91, 0.1, 0.02, 0.6])
    plt.colorbar(im, cax=axcolor)
    show()


def make_histogram(x):
    # the histogram of the data
    plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    xlabel('Similarity')
    ylabel('Probability')
    title(r'$\mathrm{Histogram\ of\ Scores:}$')
    grid(True)
    show()


def mask_correlation(i):
    if i <= .7 and i > 0:
        return 1.
    else:
        return 0.


def correlation_adjacency_matrix(correlation_matrix):
    f = np.vectorize(mask_correlation)
    return f(correlation_matrix)


def cross_correlation_graph(m_phi, coefs):
    G = nx.Graph(m_phi)
    for node in G.nodes_iter():
        G.node[node]['label'] = str(coefs.loc[node+1]['Topics'])
        G.node[node]['coeff'] = float(coefs.loc[node+1]['Estimate'])
    return G


def get_top_docs(ind, mat):
    return pd.Series([kullback_leibler(row, mat[ind]) for row in mat])

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'cache')
    phi = pd.DataFrame.from_csv(os.path.join(path, 'phi.csv'))
    theta = pd.DataFrame.from_csv(os.path.join(path, 'theta.csv'))
    s = get_top_docs(0, theta.values)
    s.to_csv(os.path.join(path, '0_top_docs.csv'))
    s2 = get_top_docs(360, theta.values)
    s2.to_csv(os.path.join(path, '360_top_docs.csv'))
    coefs = pd.DataFrame.from_csv(os.path.join(path, 'coefs.csv'))
    coefs.index = [int(ind.split('.')[2]) for ind in coefs.index]
    df_phi_adj = pd.DataFrame(pairwise_distances(phi.values, metric=cosine))
    df_phi_adj.to_csv(os.path.join(path, "adjacency_matrix_phi.csv"))
    G = cross_correlation_graph(df_phi_adj.values, coefs)
    nx.write_gexf(G, os.path.join(path, 'phi.gexf'))
    make_histogram([item for sublist in df_phi_adj.values for item in sublist])
    make_good_heatmap(df_phi_adj.values)
    pd_phi_mask = correlation_adjacency_matrix(df_phi_adj)
    make_heatmap(pd_phi_mask)
