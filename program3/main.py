import sys
import re
from math import log
from collections import defaultdict

non_alphanum = re.compile(r'[\W_]+')
flatten = lambda l: [item for sublist in l for item in sublist]

def process_word(word):
    return non_alphanum.sub('', word.lower())

def process_document(document):
    """returns a tuple. the first element is the review split into an array of words
    the second element is an int indicating if the review was positive """
    return (
        [process_word(word) for word in document.split()][:-1],
        int(document.split()[-1])
    )

def format_document(document, vocab):
    return (
        ','.join(['1' if word in document[0] else '0' for word in vocab])
        + ',' + str(document[1])
    )

def preprocess(infilename, outfilename):
    """ returns a tuple in the for of (vocab, documents).
    vocab: a set of words such as {'great', 'steak', 'gross', ...}
    documents: a tuple containing the array of words in the document followed 
    by the sentiment of the document, represented by a 1 or 0
    where 1 is liked and 0 is disliked """

    #process input file
    infile = open(infilename, 'r')
    raw_documents = infile.read().splitlines()
    documents = [process_document(document) for document in raw_documents]
    vocab = {process_word(word) for document in raw_documents for word in document.split()[:-1]}
    vocab.discard('')
    infile.close()

    #format text for outfile and write
    outfile = open(outfilename, 'w')
    formatted_vocab = ','.join(sorted(list(vocab)))
    formatted_documents = '\n'.join([format_document(document, vocab) for document in documents])
    outfile.write(formatted_vocab + '\n' + formatted_documents)
    outfile.close()

    return vocab, documents

def train_naive_bayes(vocab, documents, classes):
    logprior = {}
    loglikelihood = defaultdict(dict)
    big_doc = {}

    def get_logprior(documents, c):
        class_document_count = len([doc for doc in documents if doc[1] == c])
        total_document_count = len(documents)
        return log(class_document_count / total_document_count)

    def get_bigdoc(documents, c):
        return flatten([doc[0] for doc in documents if doc[1] == c])

    for c in classes:
        logprior[c] = get_logprior(documents, c)
        big_doc[c] = get_bigdoc(documents, c)
        words_in_class_count = sum([big_doc[c].count(w) for w in vocab])

        for word in vocab:
            word_count = big_doc[c].count(word)
            loglikelihood[word][c] = log((word_count + 1) / (words_in_class_count + 1))

    return logprior, loglikelihood

def test_naive_bayes(document, logprior, loglikelihood, classes, vocab):
    #filter word not in the vocab
    document = [word for word in document[0] if word in vocab]
    prob = {}

    for c in classes:
        prob[c] = logprior[c]
        for word in document:
            prob[c] = prob[c] + loglikelihood[word][c]

    return max(prob.keys(), key=(lambda key: prob[key]))

def print_test_results(results, test_docs):
    misclassified_docs = []
    for result, doc in zip(results, test_docs):
        if result != doc[1]:
            misclassified_docs.append(doc + tuple([result]))

    for doc in misclassified_docs:
        print('misclassified {}: actual: {}, expected: {}'.format(doc[0], doc[2], doc[1]))

    correct = len(test_docs) - len(misclassified_docs)
    incorrect = len(misclassified_docs)
    accuracy = correct / len(test_docs)

    print("\n")
    print("****************************************")
    print("* RESULTS:")
    print("*     Correct:   {}".format(correct))
    print("*     Incorrect: {}".format(incorrect))
    print("*")
    print("*     Accuracy:  {}".format(accuracy))
    print("****************************************")

def test(test_docs, prior, likelihood, classes, vocab):
    results = []
    for test_doc in test_docs:
        results.append(test_naive_bayes(test_doc, prior, likelihood, classes, vocab))
    print_test_results(results, test_documents)

#prevent running if imported as a module
if __name__ == '__main__':
    classes = [0, 1]
    # perform test on the training data
    sys.stdout = open('results.txt', 'wt')
    vocab, documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')
    _, test_documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')

    prior, likelihood = train_naive_bayes(vocab, documents, classes)

    print("\n")
    print("testing on training data")
    test(documents, prior, likelihood, classes, vocab)

    # perform test on the testing data
    vocab, documents = preprocess('trainingSet.txt', 'preprocessed_train.txt')
    _, test_documents = preprocess('testSet.txt', 'preprocessed_test.txt')

    prior, likelihood = train_naive_bayes(vocab, documents, classes)
    print("\n")
    print("testing on testing data")
    test(test_documents, prior, likelihood, classes, vocab)