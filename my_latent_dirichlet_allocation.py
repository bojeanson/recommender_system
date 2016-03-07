from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
from time import time


def print_top_words(lda_model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(lda_model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

def get_similar(doc_id, doc_topic_distribution):
    doc_rep = np.array([doc_topic_distribution[doc_id]]*len(doc_topic_distribution))
    sim = np.dot(((np.log(doc_rep)-np.log(doc_topic_distribution))),doc_topic_distribution[doc_id])
    return sim.argsort()


class MyLatentDirichletAllocation(object):

    def __init__(self, jokes_words, n_topics=20, doc_topic_prior=None, topic_word_prior=None, learning_method='online', learning_decay=0.7, learning_offset=10.0, max_iter=10, batch_size=128, evaluate_every=-1, total_samples=1000000.0, perp_tol=0.1, mean_change_tol=0.001, max_doc_update_iter=100, n_jobs=1, verbose=0, random_state=None):
        t0 = time()
        self.K = n_topics
        self.model = LatentDirichletAllocation(n_topics, doc_topic_prior, topic_word_prior, learning_method, learning_decay, learning_offset, max_iter, batch_size, evaluate_every, total_samples, perp_tol, mean_change_tol, max_doc_update_iter, n_jobs, verbose, random_state).fit(jokes_words)
        print("done in %0.3fs." % (time() - t0))