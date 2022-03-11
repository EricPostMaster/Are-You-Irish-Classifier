import streamlit as st
import pickle
import re
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB

# Unpickle the Pipeline object
with open("pickled_CompNB_model.p", "rb") as p:
    model = pickle.load(p)

with open("irish_log_probs.p", "rb") as p:
    feature_probs = pickle.load(p)


def ngram_creator(term_list, n=4):
    """
    Takes two arguments: a list of words to break into ngrams and the length of the ngram

    Inputs:
        term_list: [list] terms to break into intraword ngrams (example: df['names'])
        n: [int] desired length of ngrams
    
    Outputs:
        ngrams of individual words: e.g., bigrams for 'dog' = ['do','og']
        gram_string_list: list where each element is the set of n-grams for each original record. Use in CountVectorizer
    """

    gram_string_list = []
    gram_length = n

    for i in term_list:
        i = str(i)
        i = re.sub('[^A-Za-z0-9]+', '', i) # Remove any punctuation, spaces, and special characters
    
        i = i.lower()
        i = " "+i+" "  # Add initial and terminal clusters

        # break
        word_grams = []
        gram_string = ""
        for j in range(gram_length,100):
            gram = i[j-gram_length:j]
            if len(gram) == gram_length:  # only keep ngrams of the correct length
                word_grams.append(gram)
                gram_string = gram_string + gram + " "
        gram_string = gram_string[:-1]  # Cut that last space off the end there
        gram_string_list.append(gram_string)  # Append the ngrams for the current name as a space-separated string
    
    return word_grams #gram_string_list



# App title, favicon
st.set_page_config(
	page_title="How Irish Are You??? Discover your Murphy Score today!",
	page_icon=":shamrock:",
	layout="centered"
)





#########################################################################################
# Streamlit app begins
#########################################################################################

st.title("""How Irish is your surname? - Find out with the Murphy Index!""")

st.subheader("How it works:")
st.write("""This super fancy tool is powered by three things:
- Machine learning
- Bayesian statistics
- Grossly violated assumptions of independence
It will read your surname, crunch numbers like a boss, and give you the one thing you've never
had but always needed: **your Murphy Score**. It's a score that tells you how Irish your
name is relative to the most Irish of names: *Murphy*.""")
st.write("""What are you waiting for? Type your surname below and hit Enter!""")



user_name = [st.text_input('Your last name')]
if user_name:
    # Predict it with the model.
    # st.write(model.predict_proba(user_name))
    ngram_list = ngram_creator(user_name)

    # st.write(feature_probs[0:2])
    # st.write(list(filter(lambda prob: prob[0] == ' sim', feature_probs))[0][1])
    # st.write(ngram_list[0])

    attempted_flag = 0
    ngrams_and_probs = []
    for ngram in ngram_list:
        try:
            p = list(filter(lambda prob: prob[0] == ngram, feature_probs))[0][1]
            ngrams_and_probs.append([ngram, p])
        except:
            attempted_flag = 1
            continue

    # st.write(ngrams_and_probs)

    user_name_log_probs = [p for _, p in ngrams_and_probs]

    # st.write(user_name_log_probs)
    if len(ngrams_and_probs) > 0:

        user_name_avg_log_prob = sum(user_name_log_probs) / float(len(ngrams_and_probs))

        murphy_score = round((6.58 / user_name_avg_log_prob)*-100,2)

        st.write(f"Your Murphy Score is: {murphy_score}/100!")
        st.write("That's definitely good enough for a drink! :shamrock: :beers:")
    
    elif attempted_flag == 1:
        st.write("Well, Janey Mack, look at that! We've never seen a name like yours!")
        st.write("Even so, it'd be a pity to leave a jar lonely on St. Patty's Day, so drink up! :beers:")
    
    else:
        st.write(f"Your Murphy Score is: ___/100")
    # Take each element of the user_name list and get the log probability from feature_probs

    # Calculate the average log_probability of the absolute values of each probability


    # If none are there, then return a statement like,
        # "Well, Janey Mack, look at that! We've never seen a name like yours!"