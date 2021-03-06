# Implement SKLEARN LatentDirichletAllocation with varitional Bayes on the 20NewsGroup dataset
# Ref: Olivier Grisel 
#      Lars Buitinck
#      Chyi-Kwei Yau 
# License: BSD 3 clause
from src.utility import *
from Comparisons.print_sklearn import*
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from time import time

n_samples = 10
n_topics = 20


# Load the 20 newsgroups dataset and vectorize it. We use a few heuristics
# to filter out useless terms early on: the posts are stripped of headers,
# footers and quoted replies, and common English words, words occurring in
# only one document or in at least 95% of the documents are removed.

if __name__ == '__main__':

    # For version before .22
    dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))

    data = dataset['data']
    # Putting each doc in an ordered dictionnary
    title_docs = {}
    for i in range(len(data)):
            title_docs[i] = data[i]
    ###### First get the data ready similarly to our implemented example          
    titles_to_tokens = {title: tokenize_doc(doc) for title, doc in title_docs.items()}
    # Remove articles whose content is 'blah blah blah'
    extra_words = ['maxaxaxaxaxaxaxaxaxaxaxaxaxaxax', 'said', 'also', 'would', 'get', 'say', 'go', 'do', 'one']
    titles_to_tokens = {title: remove_stop_words(tokens, extra_words=extra_words)
                        for title, tokens in titles_to_tokens.items() if 'blah' not in tokens}
    titles_to_tokens_stem = {title: stem_tokens(tokens) for title, tokens in titles_to_tokens.items()}
    
    # Transforming the data to a list of texts according to the required format for the count vectorizer
    data_skl = list(titles_to_tokens_stem.values())
    for i in range(len(data_skl)):
        data_skl[i] = ' '.join((  # note double parens, join() takes an iterable
            data_skl[i]
        ))
    # Getting list of doc titles 
    docs_skl = list(titles_to_tokens_stem)
 
    ##### Second run the algorithm
    t0 = time()
    # Use tf (raw term count) features for LDA.
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer()

    tf = tf_vectorizer.fit_transform(data_skl)

    print("Fitting LDA models "
          "n_samples=%d ..."
          % (n_samples))
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=n_samples,
                                    learning_method='online',
                                    random_state=0)
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))
    
    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    n_top_words = 5
    print_top_words(lda, tf_feature_names, n_top_words)
    
    doc_n = 0 # get topics for a given doc:
    print("\nTopics in Doc %s :" % docs_skl[doc_n])
    topics_spec_doc(lda, tf, n_topics, doc_n)
