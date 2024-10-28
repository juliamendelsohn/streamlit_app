import streamlit as st
import plotly.express as px
from visualize_log_odds import visualize_all_tabs, load_data


log_odds_dir = 'results/log_odds/speeches/'
filename = 'trump_harris.csv'
corpus1_name = "Trump"
corpus2_name = "Harris"
st.header(f"Campaign Speeches (Trump vs. Harris)")
st.write("This page visualizes the log-odds ratio of words between the two corpora.\
        Log-odds ratio is a measure of the strength of association between a word and a corpus.")

df_dict = load_data(log_odds_dir,filename)
reversed_color = px.colors.diverging.RdYlBu[::-1]
visualize_all_tabs(df_dict,corpus1_name,corpus2_name,color_scale=reversed_color)