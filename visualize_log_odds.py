import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px

@st.cache_data
def load_data(log_odds_dir,filename):
    df_dict = {}
    df_dict['unigram'] = pd.read_csv(os.path.join(log_odds_dir,'ngram_1/stopwords_english',filename))
    df_dict['bigram'] = pd.read_csv(os.path.join(log_odds_dir,'ngram_2/stopwords_english',filename))
    df_dict['nouns'] = pd.read_csv(os.path.join(log_odds_dir,'noun',filename))
    df_dict['verbs'] = pd.read_csv(os.path.join(log_odds_dir,'verb',filename))
    df_dict['adjectives'] = pd.read_csv(os.path.join(log_odds_dir,'adjective',filename))
    return df_dict

def df_filter(df,corpus1_name,corpus2_name,selection):
    row_input = st.columns((1,1))
    with row_input[0]:
        key = f"{selection}_min_{corpus1_name}"
        number = st.number_input(f"{corpus1_name} Min Word Count",max_value=df['count 1'].max(),key=key)
        df = df[df['count 1'] >= number]
                
    with row_input[1]:
        key = f"{selection}_min_{corpus2_name}"
        number = st.number_input(f"{corpus2_name} Min Word Count",max_value=df['count 2'].max(),key=key)
        df = df[df['count 2'] >= number]
    return df


def plot_log_odds(df,corpus1_name,corpus2_name,color_scale):
    # Create a scatterplot with interactive tooltips
    fig = px.scatter(df, x='total_count', y='log_odds', #text='term', 
                    color='log_odds', #width=1000, height=100,
                    color_continuous_scale=color_scale,
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
    st.plotly_chart(fig,use_container_width=True)
    
def select_and_plot(df_dict,corpus1_name,corpus2_name,selection,color_scale):
    df = df_dict[selection]
    df['total_count'] = df['count 1'] + df['count 2']
    df = df_filter(df,corpus1_name,corpus2_name,selection)
    # Add radio button for showing data or plotting
    show_plot = st.radio("Show plot or table",('Plot', 'Table'),key=selection,horizontal=True)
    if show_plot == 'Table':
        df_condensed = df[['term','log_odds','count 1','count 2','total_count']]
        df_condensed.columns = ['Term','Log-Odds',f'{corpus1_name} Count',f'{corpus2_name} Count','Total Count']
        st.write(df_condensed)
    else:
        plot_log_odds(df,corpus1_name,corpus2_name,color_scale)

def visualize_all_tabs(df_dict,corpus1_name,corpus2_name,color_scale=px.colors.diverging.RdYlBu):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Words (excl. stop words)", "1-2 Word Phrases","Nouns","Verbs","Adjectives"])
    with tab1:
        select_and_plot(df_dict,corpus1_name,corpus2_name,'unigram',color_scale)
    with tab2:
        select_and_plot(df_dict,corpus1_name,corpus2_name,'bigram',color_scale)
    with tab3:
        select_and_plot(df_dict,corpus1_name,corpus2_name,'nouns',color_scale)
    with tab4:
        select_and_plot(df_dict,corpus1_name,corpus2_name,'verbs',color_scale)
    with tab5:
        select_and_plot(df_dict,corpus1_name,corpus2_name,'adjectives',color_scale)


