import streamlit as st
from visualize_log_odds import visualize_all_tabs, load_data

st.markdown("""
        <style>
               .block-container {
                    padding-top: 2rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

log_odds_dir = 'results/log_odds/platforms/'
filename = 'democrat_2024_democrat_2020.csv'
corpus1_name = "2024"
corpus2_name = "2020"
df_dict = load_data(log_odds_dir,filename)
visualize_all_tabs(df_dict,corpus1_name,corpus2_name)