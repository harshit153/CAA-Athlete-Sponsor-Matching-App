import streamlit as st
import pandas as pd
import sklearn as sk
import numpy as np
def load_data():
    dfcompatt = pd.read_csv("data/company_attributes2.csv", index_col=0)
    return dfcompatt
def load_more_data():
    df_combined = pd.read_csv("data/df_combined.csv")
    return df_combined
def app():
    dfcompatt = load_data()
    tab_cluster_search, tab_athlete, tab_filter  = st.tabs(["Search by Cluster", "Training Data", "Filter by Characteristics"])
    with tab_cluster_search:
        dfcompatt = dfcompatt.rename(columns = {"Kmeans": "Company_Cluster"})
        st.subheader('Sort by Cluster')
        st.text("We clustered the companies in our data into 5 distinguishable groups labeled 0-5.")
        cluster = st.selectbox("Choose a cluster:", dfcompatt.Company_Cluster.sort_values(ascending=True).unique(), index=0)
        player_info = dfcompatt[dfcompatt.Company_Cluster == cluster]
        st.dataframe(player_info, height = 500)
    with tab_athlete:
        st.subheader('Training Data')
        df_combined = load_more_data()
        df_combined = df_combined.rename(columns = {"Kmeans": "Company_Cluster"})
        st.dataframe(df_combined, height = 500)
    with tab_filter:
        features = st.subheader('Filter by Athlete Characteristics')
        st.write("School")
        schools = st.selectbox("Choose a school (or start typing):", df_combined.School.sort_values(ascending = True).unique(), index=0)
        st.markdown("---")
        st.write("NIL Value")
        nil = st.text_input('NIL Value', '')
        st.markdown("---")
        st.write("Instagram Followers")
        instagram = st.text_input('Number of Instagram Followers', '')
        st.markdown("---")
        st.write("Twitter Followers")
        twitter = st.text_input('Number of Twitter Followers', '')
        st.markdown("---")
        st.write("TikTok Followers")
        tiktok = st.text_input('Number of TikTok Followers', '')
        st.markdown("---")
        st.header("Predicted Cluster:")
        #Model
        # formatting intput data
        schools_col = df_combined.School.sort_values(ascending = True).unique()
        temp_c = np.array(['NIL value', 'Instagram Followers', 'TikTok Followers', 'Twitter Followers'])
        cols = np.append(temp_c, schools_col)
        input_data = {}
        for c in cols:
            input_data[c] = 0
        input_data['NIL value'] = nil
        input_data['Instagram Followers'] = instagram
        input_data['TikTok Followers'] = tiktok
        input_data['Twitter Followers'] = twitter
        input_data[schools] = 1
        actual_input = [list(input_data.values())]
        target = df_combined['Company_Cluster']
        data_for_model=df_combined[[ 'School','NIL value', 'Instagram Followers', 'TikTok Followers', 'Twitter Followers']]
        for i in [ 'NIL value', 'Instagram Followers', 'TikTok Followers', 'Twitter Followers']:
            data_for_model[i] = data_for_model[i].fillna(data_for_model[i].median())
        data_for_model = pd.get_dummies(data_for_model)
        # Import train_test_split function
        from sklearn.model_selection import train_test_split
        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(data_for_model, target, test_size=0.3)
        # 70% training and 30% test
        #Import Random Forest Model
        from sklearn.ensemble import RandomForestClassifier
        #Create a Random Forest Classifier with 100 trees
        clf=RandomForestClassifier(n_estimators=300, n_jobs=-1)
        #Train the model using the training sets y_pred=clf.predict(X_test)
        clf.fit(X_train,y_train)
        if nil and instagram and tiktok and twitter and schools:
            y_pred=clf.predict(actual_input)
            st.subheader(y_pred)
