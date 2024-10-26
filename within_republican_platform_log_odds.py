import streamlit as st
from visualize_log_odds import visualize_all_tabs, load_data


log_odds_dir = 'results/log_odds/platforms/'
filename = 'republican_2024_republican_2016.csv'
corpus1_name = "2024"
corpus2_name = "2016/2020"
st.header(f"Republican Platforms (2024 vs 2016/2020)")
st.write("This page visualizes the log-odds ratio of words between the two corpora.\
        Log-odds ratio is a measure of the strength of association between a word and a corpus.")

df_dict = load_data(log_odds_dir,filename)
visualize_all_tabs(df_dict,corpus1_name,corpus2_name)