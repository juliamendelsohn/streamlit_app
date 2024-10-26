import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px

@st.cache_data
def load_data(log_odds_dir,filename):
    df_dict = {}
    df_dict['unigram'] = pd.read_csv(os.path.join(log_odds_dir,'ngram_1/stopwords_None',filename))
    df_dict['unigram_stop'] = pd.read_csv(os.path.join(log_odds_dir,'ngram_1/stopwords_english',filename))
    df_dict['nouns'] = pd.read_csv(os.path.join(log_odds_dir,'noun',filename))
    df_dict['verbs'] = pd.read_csv(os.path.join(log_odds_dir,'verb',filename))
    df_dict['adjectives'] = pd.read_csv(os.path.join(log_odds_dir,'adjective',filename))
    return df_dict

def df_filter(df,corpus1_name,corpus2_name):
    row_input = st.columns((1,1))
    with row_input[0]:
        number = st.number_input(f"{corpus1_name} Min Word Count",max_value=df['count 1'].max())
        df = df[df['count 1'] >= number]
                
    with row_input[1]:
        number = st.number_input(f"{corpus2_name} Min Word Count",max_value=df['count 2'].max())
        df = df[df['count 2'] >= number]
    return df


def plot_log_odds(df,corpus1_name,corpus2_name):
    # Create a scatterplot with interactive tooltips
    fig = px.scatter(df, x='total_count', y='log_odds', #text='term', 
                    color='log_odds', width=900, height=600,
                    color_continuous_scale=px.colors.diverging.RdYlBu,
                    opacity=1, color_continuous_midpoint=0,range_color=[-4,4],
                    hover_name='term', log_x=True, log_y=False, 
                    hover_data={'log_odds': ':.2f',
                                'total_count': False,
                                'term': False,
                                }
                    )
    fig.update_traces(marker=dict(size=10))  # Set all points to size 10
    fig.update(layout_coloraxis_showscale=False)
    
    fig.update_layout(
        yaxis_title=f"<-- More {corpus2_name.split()[0]}                   Log-Odds                          More {corpus1_name.split()[0]} -->",
        xaxis_title="Total Word Count (log scale)",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
        ),
    )
    st.plotly_chart(fig)
    


log_odds_dir = 'results/log_odds/platforms/'
filename = 'democrat_2024_republican_2024.csv'
corpus1_name = "Democratic Party 2024"
corpus2_name = "Republican Party 2024"
st.header(f"Democratic vs. Republican Platforms (2024)")
st.write("This page visualizes the log-odds ratio of words between the two corpora.\
        Log-odds ratio is a measure of the strength of association between a word and a corpus.")

df_dict = load_data(log_odds_dir,filename)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Words (incl. stop words)", "Words (excl. stop words)","Nouns","Verbs","Adjectives"])

with tab1:
    st.write("Plotting words (incl. stop words)")
    df = df_dict['unigram']
    df['total_count'] = df['count 1'] + df['count 2']
    df = df_filter(df,corpus1_name,corpus2_name)
    plot_log_odds(df,corpus1_name,corpus2_name)

with tab2:
    st.write("Plotting words (excl. stop words)")
    df = df_dict['unigram_stop']
    df['total_count'] = df['count 1'] + df['count 2']
    df = df_filter(df,corpus1_name,corpus2_name)
    plot_log_odds(df,corpus1_name,corpus2_name)

with tab3:
    st.write("Plotting nouns")
    df = df_dict['nouns']
    df['total_count'] = df['count 1'] + df['count 2']
    df = df_filter(df,corpus1_name,corpus2_name)
    plot_log_odds(df,corpus1_name,corpus2_name)

with tab4:
    st.write("Plotting verbs")
    df = df_dict['verbs']
    df['total_count'] = df['count 1'] + df['count 2']
    df = df_filter(df,corpus1_name,corpus2_name)
    plot_log_odds(df,corpus1_name,corpus2_name)

with tab5:
    st.write("Plotting adjectives")
    df = df_dict['adjectives']
    df['total_count'] = df['count 1'] + df['count 2']
    df = df_filter(df,corpus1_name,corpus2_name)
    plot_log_odds(df,corpus1_name,corpus2_name)


