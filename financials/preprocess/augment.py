# coding=utf-8
import pandas as pd
import pdb
from slugify import slugify
import os
from datetime import datetime
# from datetime import strptime

def augment(dfs):
    """
    Insert here code to augment your data frames during preprocessing
    """

    ipi = dfs['ipi']
    ipc = dfs['ipc']
    tx_chomage = dfs['tx_chomage']
    smic = dfs['smic']
    dette = dfs['dette']
    data_bourso = dfs['data_bourso']
    sectors = dfs['sectors']
    cotation = dfs['cotation']

    ipi = clean_ipi(ipi)
    ipc = clean_ipc(ipc)
    tx_chomage = clean_chomage(tx_chomage)
    smic = clean_smic(smic)
    dette = clean_dette(dette)
    data_bourso = clean_bourso(data_bourso,sectors)
    cotation = clean_cotation(cotation)
    economy = pd.concat([ipi,ipc,tx_chomage,smic,dette])
    economy['date'] = economy['mois'].astype(str) + "/" + economy['annee'].astype(str)
    pd.to_datetime(economy['date'],format="%m/%Y")
    waterfall_effectif = data_bourso[(data_bourso['metric']==u"Effectif en fin d'année")]
    # waterfall_effectif = create_waterfall(waterfall_effectif,'value','year','2014','2015','supersector','company',sectors)
    dfs['economy'] = economy
    dfs['data_bourso'] = data_bourso
    dfs['cotation'] = cotation
    # Add domain to each dataframe
    for domain, df in dfs.iteritems():
        df['domain'] = domain


    return dfs

def create_waterfall(df,value_col,diff_column,diff_value_1,diff_value_2,main_cat_col,sub_cat_col,df_meta):

    df = df[(df[diff_column]==diff_value_1)|(df[diff_column]==diff_value_2)]

    #create dataframe of evolution of sub categories
    df_sub = pd.pivot_table(df,values=value_col, index=[main_cat_col,sub_cat_col], columns=diff_column)
    df_sub['value'] = df_sub[diff_value_2]-df_sub[diff_value_1]
    df_sub = df_sub.reset_index()
    df_sub['drill_level'] = 1
    df_sub['label']= df_sub[sub_cat_col]
    df_sub = df_sub(['main_cat_col','sub_cat_col','value','drill_level',diff_value_2,diff_value_1])

    #create agregate category df
    df_main = df_sub.groupby([main_cat_col]).sum()
    df_main['drill_level'] = 0
    df_main = df_main.reset_index()
    df_main['label']= df_main[main_cat_col]

    #create initial and final State
    df_start= df[df[diff_column]==diff_value_1]
    df_start = df_start.groupby([diff_column]).sum()
    df_start['drill_level'] = -1
    df_start['label'] = diff_value_1
    df_start[main_cat_col] = 'start'
    df_start = df_start.reset_index()

    df_final= df[df[diff_column]==diff_value_2]
    df_final = df_final.groupby([diff_column]).sum()
    df_final['drill_level'] = -1
    df_final['label'] = diff_value_2
    df_final[main_cat_col] = 'end'
    df_final = df_final.reset_index()


    import ipdb; ipdb.set_trace()
    #concat
    df_start = df_start[[main_cat_col,sub_cat_col,'drill_level','label','value']]
    con = pd.concat([df_start,df_sub,df_main,df_final])
    import ipdb; ipdb.set_trace()
    return df

def clean_ipi(df):
    df.rename(columns = {'Unnamed: 2':'value'}, inplace=True)
    df.columns = df.columns.map(slugify_with_underscore)
    df['breakdown'] = 'IPI'
    return df

def clean_ipc(df):
    df.rename(columns = {'Unnamed: 2':'value'}, inplace=True)
    df.columns = df.columns.map(slugify_with_underscore)
    df['breakdown'] = 'IPC'
    return df

def clean_chomage(df):
    df.rename(columns = {'Unnamed: 2':'value'}, inplace=True)
    df['Trimestre'] = df['Trimestre'] * 3
    df.columns = df.columns.map(slugify_with_underscore)
    df.rename(columns = {'trimestre':'mois'}, inplace=True)
    df['breakdown'] = 'Unemployment rate'
    return df

def clean_smic(df):
    df.rename(columns = {'Unnamed: 2':'value'}, inplace=True)
    df.columns = df.columns.map(slugify_with_underscore)
    df['breakdown'] = 'SMIC'
    return df

def clean_dette(df):
    df.rename(columns = {'Unnamed: 2':'value'}, inplace=True)
    df['Trimestre'] = df['Trimestre'] * 3
    df.columns = df.columns.map(slugify_with_underscore)
    df.rename(columns = {'trimestre':'mois'}, inplace=True)
    df['breakdown'] = 'Dette'
    return df

def clean_bourso(df,df_sector):
    df['date'] = df['date'].apply(parse_date)
    df = df.dropna(subset=['value'])
    df['value'] = df['value'].str.replace(',','.').str.replace(' ','').astype(float)
    df = pd.merge(df,df_sector,how='left',left_on='company',right_on='company')
    df['year'] = df['date'].apply(lambda x: str(x.year))
    return df

def clean_cotation(df):
    df['month']= df['date'].apply(lambda x: str(x.month))
    df['year']= df['date'].apply(lambda x: str(x.year))
    df = df.groupby(['year','month']).mean()
    df = df.reset_index()
    return df

def parse_date(x):
    try:
        return datetime.strptime(str(x),'%m.%y')
    except Exception:
        return datetime.strptime(str(int(x)),'%Y')

def slugify_with_underscore(x):
    return  slugify(unicode(x)).replace('-','_')
