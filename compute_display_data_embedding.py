from sklearn import (manifold, datasets, decomposition, ensemble, discriminant_analysis, random_projection)
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from my_latent_dirichlet_allocation import *
from tsne import tsne as tsne_py


def compute_latent_dirichlet_allocation(X, n_topics=20, doc_topic_prior=None, topic_word_prior=None, learning_method='online', learning_decay=0.7, learning_offset=10.0, max_iter=10, batch_size=128, evaluate_every=-1, total_samples=1000000.0, perp_tol=0.1, mean_change_tol=0.001, max_doc_update_iter=100, n_jobs=1, verbose=0, random_state=None):
    print("Computing latent dirichlet allocation")
    myLDA = MyLatentDirichletAllocation(X, n_topics, doc_topic_prior, topic_word_prior, learning_method, learning_decay, learning_offset, max_iter, batch_size, evaluate_every, total_samples, perp_tol, mean_change_tol, max_doc_update_iter, n_jobs, verbose, random_state).model.fit(X)
    t0 = time()
    jokes_topics = myLDA.transform(X)
    return jokes_topics / jokes_topics.sum(axis=1)[:,None]

def compute_NMF(X, n_compo=2):
    model = decomposition.NMF(n_components=n_compo, init='random').fit(X)
    return model.components_

def compute_kernel_PCA(X, kern='cosine', n_compo=2):
    print("Computing Kernel PCA projection")
    return decomposition.KernelPCA(n_components=n_compo, kernel=kern).fit_transform(X)

def compute_PCA(X, n_components=2, algorithm='randomized', n_iter=5, random_state=None, tol=0.0):
    print("Computing PCA projection")
    return decomposition.TruncatedSVD(n_components, algorithm, n_iter, random_state, tol).fit_transform(X)

def compute_linear_discriminant_analysis(X, y, n_components=2):
    print("Computing Linear Discriminant Analysis projection")
    return discriminant_analysis.LinearDiscriminantAnalysis(n_components).fit_transform(X, y)

def compute_MDS(X, n_components=2, n_init=1, max_iter=100):
    print("Computing MDS embedding")
    clf = manifold.MDS(n_components, n_init, max_iter)
    return clf.fit_transform(X)

def compute_tSNE(X, no_dims=2):
    print("Computing t-SNE embedding")
    return tsne_py(X, no_dims)

def compute_tSNE2(X, n_comp=2, ini='pca'):
    print("Computing t-SNE embedding")
    tsne = manifold.TSNE(n_components=n_comp, init=ini)
    return tsne.fit_transform(X)

def plot_embedding(X, title=None):
    x_min, x_max = np.min(X, 0), np.max(X, 0)
    X = (X - x_min) / (x_max - x_min)

    plt.figure(figsize=(20, 10))
    for i in range(X.shape[0]):
        plt.text(X[i, 0], X[i, 1], str(i),
                 color=plt.cm.Set1(i / 10.),
                 fontdict={'weight': 'bold', 'size': 20})

    if hasattr(offsetbox, 'AnnotationBbox'):
        # only print thumbnails with matplotlib > 1.0
        shown_images = np.array([[1., 1.]])  # just something big
        for i in range(X.shape[0]):
            dist = np.sum((X[i] - shown_images) ** 2, 1)
            if np.min(dist) < 4e-3:
                # don't show points that are too close
                continue
            shown_images = np.r_[shown_images, [X[i]]]
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)