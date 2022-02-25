########## ngram function ##########

import re

def ngram_creator(term_list, n=3):
    """
    Takes two arguments: a list of words to break into ngrams and the length of the ngram

    Inputs:
        term_list: [list] terms to break into intraword ngrams (example: df['names'])
        n: [int] desired length of ngrams
    
    Outputs:
        ngrams of individual words: e.g., bigrams for 'dog' = ['do','og']
        gram_string_list: list where each element is the set of n-grams for each original record. Use in CountVectorizer
    """

        # email addresses - Going to hard-code disposable domains
        # email addresses - What about the ones that say 123@gmail.com??? That could still get through.
        # how to handle ngrams in the test set that aren't in the training set? Recursion? Check namespam paper.

    doc_list = []
    all_gram_list = []
    gram_string_list = []
    gram_length = n

    for i in term_list:
        i = str(i)
        i = re.sub('[^A-Za-z0-9]+', '', i) # Remove any punctuation, spaces, and special characters
        i = i.lower()
        # i = "^"+i+"$"  # Start and End characters didn't end up making a difference
        word_grams = []
        gram_string = ""
        for j in range(gram_length,100):
            gram = i[j-gram_length:j]
            # print(gram)
            if len(gram) == gram_length:  # only keep ngrams of the correct length
                word_grams.append(gram)
                all_gram_list.append(gram)
                gram_string = gram_string + gram + " "
        gram_string = [gram_string[:-1]]
        gram_string_list.append(gram_string)
        doc_list.append(word_grams)
    
    return gram_string_list