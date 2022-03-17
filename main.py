import streamlit as st
import pandas as pd
import pickle
import re
import time
from datetime import date
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB
import plotly.express as px

from gspread_pandas import Spread,Client
from google.oauth2 import service_account

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
workbookname = 'stored_scores'
scores_sheet = 'scores'
spread = Spread(workbookname,client = client)

sh = client.open(workbookname)
worksheet_list = sh.worksheets()


# Get the sheet as dataframe
def load_the_spreadsheet(workbookname):
    worksheet = sh.worksheet(scores_sheet)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(workbookname,dataframe_master, dataframe_new):
    col = ['score','date']
    dataframe_master = pd.concat([dataframe_master, dataframe_new], ignore_index=True, axis=0)
    spread.df_to_sheet(dataframe_master[col],sheet = scores_sheet,index = False)
    return dataframe_master



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


# Unpickle ngram log probabilities
with open("saved-objects/irish_log_probs.p", "rb") as p:
    feature_probs = pickle.load(p)


# App title, favicon
st.set_page_config(
	page_title="How Irish Are You??? Discover your Murphy Score today!",
	page_icon=":shamrock:",
	layout="centered"
)

st.markdown(
    """
    <style>
        .stProgress > div > div > div > div {
            background-color: #86CE00;
        }
    </style>""",
    unsafe_allow_html=True,
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

        my_bar = st.progress(50)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1)

        user_name_avg_log_prob = sum(user_name_log_probs) / float(len(ngrams_and_probs))

        murphy_score = round((6.56 / user_name_avg_log_prob)*-100,2)

        st.write(f"Your Murphy Score is: {murphy_score}/100!")
        st.write("That's definitely good enough for a drink! :shamrock: :beers:")
        st.write("Compare your Murphy Score to others! :point_down: :point_down: ")

        today = date.today().strftime("%m/%d/%Y")
        # Date has to be stored as a string for now
        # (https://stackoverflow.com/questions/69578431/how-to-fix-streamlitapiexception-expected-bytes-got-a-int-object-conver)
        df_murphy = pd.DataFrame({'score': [murphy_score],
                                  'date' : [today]})
        
        # Load all previous data
        df_all_data = load_the_spreadsheet(workbookname)

        # Add the new score to the master list
        # You can use this dataframe for data visualizations
        df_updated_data = update_the_spreadsheet(scores_sheet,df_all_data, df_murphy)



        fig = px.histogram(df_all_data
                           ,x='score'
                           ,nbins=12
                           ,color_discrete_sequence=['#86CE00']
                           ,title='Spread of all user Murphy Scores'
                           ,labels={'score':'Murphy Scores'}
                           ,opacity=0.7
                           )
        fig.update_traces(xbins=dict( # bins used for histogram
        start=50.0,
        end=105.0,
        size=2.5
        ))
        fig.update_layout(bargap=0.2)
        fig.add_vline(x=murphy_score
                     ,line_dash='dash'
                     ,annotation_text=f"Your Score: {murphy_score}"
                     ,annotation_position='top right'
                     ,annotation_font_size=16
                     )
        st.plotly_chart(fig, use_container_width=True)

        info_note = '<p style="font-size: 10px;">Note: No name information is stored, just your awesome Murphy Score</p>'
        st.markdown(info_note, unsafe_allow_html=True)

        # st.dataframe(df_updated_data)

    # If something other than the initial empty name field has been entered but there were no ngram matches
    elif attempted_flag == 1:
        st.write("Well, Janey Mack, look at that! We've never seen a name like yours!")
        st.write("Even so, it'd be a pity to leave a jar lonely on St. Patty's Day, so drink up! :beers:")
    
    # The page starts with this
    else:
        st.write(f"Your Murphy Score is: ___/100")