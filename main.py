import streamlit as st
import pickle
import re
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB

# Unpickle the Pipeline and log probabilities objects
with open("saved-objects/pickled_CompNB_model.p", "rb") as p:
    model = pickle.load(p)
with open("saved-objects/irish_log_probs.p", "rb") as p:
    feature_probs = pickle.load(p)


def ngram_creator(term_list, n=4):
    """
    Return list of ngrams for given term(s)

    Parameters
        term_list: list of terms to break into ngrams (e.g., ['Murphy'])
        n: int for the length of ngrams
    
    Returns
        word_grams: list of ngrams of individual words:
            e.g., 4grams for 'Murphy' = [' mur','murp','urph','rphy','phy ']
    """

    # gram_string_list = []
    # gram_length = n

    for i in term_list:
        i = str(i)
        i = re.sub('[^A-Za-z0-9]+', '', i) # Remove any punctuation, spaces, and special characters
    
        i = i.lower()
        i = " "+i+" "  # Add initial and terminal clusters

        word_grams = []
        gram_string = ""
        for j in range(n,100):
            gram = i[j-n:j]
            if len(gram) == n:  # only keep ngrams of the correct length
                word_grams.append(gram)
                gram_string = gram_string + gram + " "
        # gram_string = gram_string[:-1]  # Cut that last space off the end there
        # gram_string_list.append(gram_string)  # Append the ngrams for the current name as a space-separated string
    
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
    # Ngrams for the user's name input
    ngram_list = ngram_creator(user_name)

    # Compile probabilities from input name ngrams
    attempted_flag = 0
    ngrams_and_probs = []
    for ngram in ngram_list:
        try:
            p = list(filter(lambda prob: prob[0] == ngram, feature_probs))[0][1]
            ngrams_and_probs.append([ngram, p])
        except:
            attempted_flag = 1
            continue
    
    user_name_log_probs = [p for _, p in ngrams_and_probs]

    # If a name has been entered and has at least 1 probability available from the model
    if len(ngrams_and_probs) > 0:

        user_name_avg_log_prob = sum(user_name_log_probs) / float(len(ngrams_and_probs))

        murphy_score = round((6.58 / user_name_avg_log_prob)*-100,2)

        st.write(f"Your Murphy Score is: {murphy_score}/100!")
        st.write("That's definitely good enough for a drink! :shamrock: :beers:")

    # If something other than the initial empty name field has been entered but there were no ngram matches
    elif attempted_flag == 1:
        st.write("Well, Janey Mack, look at that! We've never seen a name like yours!")
        st.write("Even so, it'd be a pity to leave a jar lonely on St. Patty's Day, so drink up! :beers:")
    
    # The page starts with this
    else:
        st.write(f"Your Murphy Score is: ___/100")