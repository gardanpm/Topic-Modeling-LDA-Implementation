import numpy as np
from random import choices


def LatentDirichletAllocation(iden_to_tokens, K, alpha, niter, beta=0.01):
    ''' Perform collapsed Gibbs sampling to discover latent topics in corpus

    :param iden_to_tokens: A dictionary that maps unique identifiers to their contents
    :param K: Number of topics for LDA to discover
    :param alpha: Determines sparsity of topic distributions per document
    :param beta: Determines sparsity of word distributions per topic
    :param niter: Number of iterations to run the Gibbs sampler for
    :return: A (K x W) Nu
    '''

    titles = iden_to_tokens.keys()

    # Contains the ordered list of topics for each document
    # Dict of lists
    document_word_topics = {title: [] for title in titles}

    # Counts of each topic per document (dict of dicts)
    document_topic_counts = {title: dict.fromkeys(range(1, K + 1), 0) for title in titles}

    unique_words = get_unique_words(iden_to_tokens.values())
    W = len(unique_words)
    # Counts of each topic per word (dict of dicts)
    word_topic_counts = {word: dict.fromkeys(range(1, K + 1), 0) for word in unique_words}

    # Counts of each topic across all documents
    total_topic_counts = dict.fromkeys(range(1, K + 1), 0)

    for _ in range(niter):  # One iteration of Gibbs sampler
        for doc, words in iden_to_tokens.items():
            for i, word in enumerate(words):
                densities = np.zeros(K)
                curr_topic = document_word_topics[doc][i]
                for k in range(1, K + 1):
                    N_kj = document_topic_counts[doc].get(k, 0)
                    N_wk = word_topic_counts[word].get(k, 0)
                    N_k = total_topic_counts.get(k, 0)

                    # New draw is conditioned on everything BUT this observation
                    if curr_topic == k:
                        N_kj -= 1
                        N_wk -= 1
                        N_k -= 1

                    # Eq. 1
                    a_kj = N_kj + alpha
                    b_wk = (N_wk + beta) / (N_k + W * beta)

                    densities[k - 1] = a_kj * b_wk

                # Draw a new topic
                densities /= np.sum(densities)  # Normalize
                new_topic = choices(range(1, K + 1), densities)[0]

                if new_topic == curr_topic:
                    continue

                # Update counts
                document_word_topics[doc][i] = new_topic

                document_topic_counts[doc][curr_topic] -= 1
                document_topic_counts[doc][new_topic] += 1

                word_topic_counts[word][curr_topic] -= 1
                word_topic_counts[word][new_topic] += 1

                total_topic_counts[curr_topic] -= 1
                total_topic_counts[new_topic] += 1


def compute_phi_estimates(word_topic_counts, total_topic_counts, K, unique_words, beta):
    W = len(unique_words)
    phi_matrix = np.zeros((K, W))

    for w, word in enumerate(unique_words):
        for k in range(1, K + 1):
            N_wk = word_topic_counts[word][k]
            N_k = total_topic_counts[k]

            phi_matrix[k - 1, w] = (N_wk + beta) / (N_k + W * beta)

    return phi_matrix


def compute_theta_estimates(document_topic_counts, K, alpha):



def get_unique_words(tokens):
    unique_words = set().union(*tokens)
    return list(unique_words)