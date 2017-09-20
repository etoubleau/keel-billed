# coding=utf-8
import pandas as pd
import numpy as np
import pdb
from lib import datagenerator
import os


RENAME={
    'gross':'gross_revenue'
}

RENAME_PRETTY={
    'gross':'Gross Revenue'
}

director_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'director_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'country':'count',
    'budget':'mean',
    'title_year':'count',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'
}

time_director_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'director_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'country':'count',
    'budget':'mean',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'
}


actor_director_agg = {
    'color':'count',
    'title_year':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'director_facebook_likes':'mean',
    'cast_total_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'country':'count',
    'budget':'mean',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'

}

actor_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'cast_total_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'country':'count',
    'budget':'mean',
    'title_year':'count',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'director_name':'count',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'
}

time_actor_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'cast_total_facebook_likes':'mean',
    'director_name':'count',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'country':'count',
    'budget':'mean',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'
}

country_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'director_facebook_likes':'mean',
    'cast_total_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'budget':'mean',
    'title_year':'count',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'
}

time_country_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'director_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'director_name':'count',
    'budget':'mean',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'Action': 'sum',
     'Adventure': 'sum',
     'Animation': 'sum',
     'Biography': 'sum',
     'Comedy': 'sum',
     'Crime': 'sum',
     'Documentary': 'sum',
     'Drama': 'sum',
     'Family': 'sum',
     'Fantasy': 'sum',
     'Film-Noir': 'sum',
     'Game-Show': 'sum',
     'History': 'sum',
     'Horror': 'sum',
     'Music': 'sum',
     'Musical': 'sum',
     'Mystery': 'sum',
     'News': 'sum',
     'Reality-TV': 'sum',
     'Romance': 'sum',
     'Sci-Fi': 'sum',
     'Short': 'sum',
     'Sport': 'sum',
     'Thriller': 'sum',
     'War': 'sum',
     'Western': 'sum'
}


theme_country_agg = {
    'color':'count',
    'num_critic_for_reviews':'sum',
    'duration':'mean',
    'director_facebook_likes':'mean',
    'cast_total_facebook_likes':'mean',
    'gross':'mean',
    'genres':'count',
    'movie_title':'count',
    'budget':'mean',
    'title_year':'count',
    'imdb_score':'mean',
    'cast_total_facebook_likes':'mean',
    'color_count':'sum',
    'black_white':'sum',
    'genre_present':'sum'
}

def augment(dfs):
    """
    Insert here code to augment your data frames during preprocessing
    """

    df = dfs['source']

    df['color_count'] = df['color'] == 'Color'
    df['black_white'] = df['color'] == ' Black and White'

    df['profitability'] = df['gross'] / df['budget']
    df['gross'] = df['gross'] / 1000000
    df['budget'] = df['budget'] / 1000000

    df['title_year'] = df['title_year'].fillna(0).map(lambda x : str(int(x)))

    #splpit genres in genre columns
    genres_list = pd.Series(np.concatenate(df.genres.str.split('|'))).unique().tolist()
    for genre in genres_list:
        df[genre] = df['genres'].map(lambda x : genre in x)

    #split by actor
    TO_MELT = ['actor_2_name','actor_3_name','actor_1_name']
    actor_detail = pd.melt(
        df.copy(),
        id_vars = [c for c in df.columns if c not in TO_MELT],
        value_vars = TO_MELT,
        value_name='actor',
        var_name='actor_type'
    )

    #split by theme
    theme_detail = pd.melt(
        df.copy(),
        id_vars = [c for c in df.columns if c not in genres_list],
        value_vars = genres_list,
        value_name='genre_present',
        var_name='genre_type'
    )
    theme_detail = theme_detail[theme_detail['genre_present']>0]
    def add_profitability(df, gross='gross', budget='budget', profitability='profitability'):
        df[profitability] = df[gross] / df[budget]

    #directors
    dfs['main_director'] = df.groupby('director_name').agg(director_agg).reset_index()
    add_profitability(dfs['main_director'])
    dfs['time_director'] = df.groupby(['director_name','title_year']).agg(time_director_agg).reset_index()
    add_profitability(dfs['time_director'])
    dfs['actor_director'] = actor_detail.groupby(['director_name','actor']).agg(actor_director_agg).reset_index()
    add_profitability(dfs['actor_director'])
    #actors
    dfs['main_actor'] = actor_detail.groupby('actor').agg(actor_agg).reset_index()
    dfs['time_actor'] = actor_detail.groupby(['actor','title_year']).agg(time_actor_agg).reset_index()
    #countries
    dfs['main_country'] = df.groupby('country').agg(country_agg).reset_index()
    add_profitability(dfs['main_country'])

    dfs['time_country'] = df.groupby(['country','title_year']).agg(time_country_agg).reset_index()
    add_profitability(dfs['time_country'])
    temp = dfs['time_country'].copy()
    temp['title_year'] = temp['title_year'].map(lambda x :str(int(x)+1))
    temp.rename(columns={'gross':'previous_gross'}, inplace=True)
    temp = temp[['title_year', 'country','previous_gross']]
    dfs['time_country'] = pd.merge(temp, dfs['time_country'], on=['title_year','country'], how='outer')
    dfs['time_country']['gross_variation'] = dfs['time_country']['gross'] / dfs['time_country']['previous_gross']

    dfs['date_requester'] = pd.DataFrame(dfs['time_country']['title_year'].unique(), columns=['date'])

    dfs['theme_country'] = theme_detail.groupby(['country','genre_type']).agg(theme_country_agg).reset_index()
    dfs['theme_country']['genre_proportion'] = dfs['theme_country']['genre_present'] / dfs['theme_country']['movie_title']

    #Add reports with directors, actors and countries

    TO_MELT = ['actor_2_name','actor_3_name','actor_1_name']
    reports = pd.DataFrame({
                             'unique_id':['Synthesis'],
                             'actor':['Synthesis'],
                             'director_name':['Synthesis'],
                             'country':['Synthesis'],
                             'genre_type':['Synthesis'],
                             'movie_title':['Synthesis'],
                             })
    reports_main = pd.melt(
        theme_detail.copy(),
        id_vars = [c for c in theme_detail.columns if c not in TO_MELT],
        value_vars = TO_MELT,
        value_name='actor',
        var_name='actor_type'
    )
    reports_main.drop_duplicates(subset=['director_name','actor','movie_title'], inplace=True)
    reports_main['unique_id']=reports_main['director_name'] + reports_main['actor'] + reports_main['movie_title']
    reports = pd.concat([reports, reports_main])

    dfs['reports'] = reports

    return dfs
