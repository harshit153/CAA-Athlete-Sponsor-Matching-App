import streamlit as st
import pandas as pd
import math

SOCIAL_MEDIA_COLS = ["Instagram Followers", "Twitter Followers", "TikTok Followers"]

def load_data():
    dfplayers = pd.read_csv("data/deals.csv", index_col=0)
    return dfplayers

def format_followers(flt):
    if math.isnan(flt):
        return flt
    if flt < 1000:
        return str(int(flt))
    if flt < 100000:
        return str(round(flt / 1000, 1)) + "k"
    if flt < 1000000:
        return str(flt)[:3] + "k"
    return str(round(flt / 1000000, 1)) + "M"

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

def get_magnitude(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return magnitude

def app():
    st.header('Search for Athletes')
    tab_search, tab_filter = st.tabs(["Search by Name", "Filter by Features"])

    dfplayers = load_data()

    #select player
    with tab_search:
        st.subheader('Player Lookup')
        player = st.selectbox("Choose a player (or click below and start typing):", dfplayers.Name.unique(), index=0)

        player_deals = dfplayers[dfplayers.Name == player]
        player_info = player_deals.loc[player_deals.index[0]]

        if type(player_info['Sport']) != str:
            st.write(f'''
                     ##### <div style="font-size: 54px; font-weight: bolder;"> {player_info.Name}</div>
                     ##### <div style="font-size: 20px; color: gray; font-weight: thin;"> {player_info.School} </div>
                     ''', unsafe_allow_html=True)

        else:
            st.write(f'''
                     ##### <div style="font-size: 54px; font-weight: bolder;"> {player_info.Name}</div>
                     ##### <div style="font-size: 20px; color: gray; font-weight: thin;"> {player_info.School} ∙  {player_info.Sport} </div>
                     ''', unsafe_allow_html=True)

        igcol, twcol, ttcol, ytcol = st.columns(4)

        igcol.image("img/instagram.png", width=40)
        igcol.write(format_followers(player_info[SOCIAL_MEDIA_COLS[0]]))

        twcol.image("img/twitter.png", width=40)
        twcol.write(format_followers(player_info[SOCIAL_MEDIA_COLS[1]]))

        ttcol.image("img/tiktok.png", width=40)
        ttcol.write(format_followers(player_info[SOCIAL_MEDIA_COLS[2]]))

        #TODO: use series PLAYER_INFO to create visualizations
        st.table(player_deals[['Deal Date', 'Company']].reset_index().drop("index", axis=1))

    #filter by
    with tab_filter:
        with st.expander("Filter Results"):

            school_col, sport_col, name_col = st.columns(3)

            schools = list(dfplayers.School.unique())
            schools.sort()
            school = school_col.selectbox(
                        'University/College',
                        ["All"] + schools)

            if school == "All":
                dfdisplay = dfplayers.copy()
            else:
                dfdisplay = dfplayers[dfplayers["School"] == school]

            sport = sport_col.selectbox('Sport', ["All"] + list(dfdisplay.Sport.unique()))
            if sport != "All":
                dfdisplay = dfdisplay[dfdisplay["Sport"] == sport]

            name = name_col.selectbox('Player', ["All"] + list(dfdisplay.Name.unique()))
            if name != "All":
                dfdisplay = dfdisplay[dfdisplay["Name"] == name]

            max_ig = int(max(dfdisplay["Instagram Followers"]))
            instagram = st.slider('Instagram Followers',
                                  min_value=0, max_value=max_ig, value=(0, max_ig))
            dfdisplay = dfdisplay[(dfdisplay['Instagram Followers'] >= instagram[0]) & (dfdisplay['Instagram Followers'] <= instagram[1])]

            max_tw = int(max(dfdisplay["Twitter Followers"]))
            twitter = st.slider('Twitter Followers',
                                  min_value=0, max_value=max_tw, value=(0, max_tw))
            dfdisplay = dfdisplay[(dfdisplay['Twitter Followers'] >= twitter[0]) & (dfdisplay['Twitter Followers'] <= twitter[1])]

            max_tt = int(max(dfdisplay["TikTok Followers"]))
            tiktok = st.slider('TikTok Followers',
                                  min_value=0, max_value=max_tt, value=(0, max_tt))
            dfdisplay = dfdisplay[(dfdisplay['TikTok Followers'] >= tiktok[0]) & (dfdisplay['TikTok Followers'] <= tiktok[1])]

            total_followers = dfdisplay[["Instagram Followers", "Twitter Followers", "TikTok Followers"]].sum(axis='columns')
            max_followers = int(max(total_followers))
            followers = st.slider('Total Followers',
                                    min_value=0, max_value=max_followers, value=(0, max_followers))
            dfdisplay = dfdisplay[(total_followers >= followers[0]) & (total_followers <= followers[1])]

        #TODO: use DFMETRICS to create visualizations
        dfmetrics = dfdisplay.drop_duplicates(subset='Name')
        st.write(f'''
                 ##### <div style="font-size: 24px;"> Average Metrics</div>
                 ''', unsafe_allow_html=True)
        igcol, twcol, ttcol, ytcol = st.columns(4)

        igcol.image("img/instagram.png", width=40)
        igcol.write(format_followers(dfmetrics[SOCIAL_MEDIA_COLS[0]].mean()))

        twcol.image("img/twitter.png", width=40)
        twcol.write(format_followers(dfmetrics[SOCIAL_MEDIA_COLS[1]].mean()))

        ttcol.image("img/tiktok.png", width=40)
        ttcol.write(format_followers(dfmetrics[SOCIAL_MEDIA_COLS[2]].mean()))

        st.dataframe(dfdisplay.reset_index(drop=True), height=500)
