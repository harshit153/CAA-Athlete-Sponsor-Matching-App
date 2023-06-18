import streamlit as st
import pandas as pd

def load_data():
    dfplayers = pd.read_csv("data/deals.csv", index_col=0).reset_index(drop=True)
    return dfplayers

def app():
    st.title('Baseball College Athlete Dashboard')
    st.header('Homepage')
    st.markdown('Use this dashboard to either display information about an athlete or predict which companies would be the best fit for an athlete!')
    st.subheader('How did we select our data?')
    st.markdown('We web-scraped ~2.8K data points from On3’s NIL Deal Tracker (https://www.on3.com/nil/deals/).')
    st.markdown('')
    st.markdown('After performing k-means clustering on this dataset, we observed that there was a significantly larger cluster, where athletes had relatively low follower counts and low NIL values.')
    st.markdown('')
    st.markdown('We decided to focus on it, as it is also more relevant to this project - connecting athletes with a smaller social media presence to potential deals!')
    st.subheader('The Data')

    st.dataframe(load_data(), height=700)
