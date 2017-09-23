# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd


def prepare_growth(df):
    df['date_year'], temp = df.date.str.split('-',1).str
    df['date_filter'] = df['date_year'].map(
        lambda x : 'Avant 1913' if int(x) < 1914 else 'Après 1913'
    )
    
    COLUMNS_NAMES = {
        'r_after_taxes':'Rendement après impôts',
        'r_before_taxes':'Rendement avant impôts',
        'g':'Croissance'
    };
    
    df.rename(columns=COLUMNS_NAMES, inplace=True);

    return df

def prepare_concentration(df):

    to_melt = [x for x in df.columns if x != 'date']
    df = pd.melt(df, id_vars='date', value_vars = to_melt)
    df['zone'], df['type'] = df.variable.str.split('_',1).str

    RENAME_TYPE = {
        'top_0_1':u'Top 0,1%',
        'top_1':u'Top 1%',
        'top_10':u'Top 10%'
    }

    RENAME_ZONE = {
        'france':'France',
        'sweden':u'Suède',
        'us':'Etats Unis',
        'europe':'Europe',
        'uk':'Royaume Unis'
    }

    df.type = df.type.replace(RENAME_TYPE)
    df.zone = df.zone.replace(RENAME_ZONE)
    df = df[df.type != 'top_1_paris']

    return df

def prepare_output(df):

    to_keep = ['date',u'world_gdp_billions_2012_ppp']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt, value_name='%')
    df = df[df.variable != 'total']

    region_mapper = {
                        u'africa':'Afrique', u'america':u'Amériques', u'asia':'Asie', u'australia_nz':'Asie', u'central_asia':'Asie',
                        u'china':'Asie', u'eastern_europe':'Europe', u'europe':'Europe', u'india':'Asie', u'japan':'Asie',
                        u'latin_america':u'Amériques', u'middle_east_y_c_turkey':'Asie', u'north_america':u'Amériques',
                        u'northern_africa':'Afrique', u'other_asian_countries':'Asie',
                        u'russia_ukraine_belarus_moldavia':'Europe', u'sub_saharan_africa':'Afrique',
                        u'western_europe':'Europe', u'world':'World'
                    }

    type_mapper = {
                        u'africa':'parent', u'america':'parent', u'asia':'parent', u'australia_nz':'child', u'central_asia':'child',
                        u'china':'child', u'eastern_europe':'child', u'europe':'parent', u'india':'child', u'japan':'child',
                        u'latin_america':'child', u'middle_east_y_c_turkey':'child', u'north_america':'child',
                        u'northern_africa':'child', u'other_asian_countries':'child',
                        u'russia_ukraine_belarus_moldavia':'child', u'sub_saharan_africa':'child',
                        u'western_europe':'child', u'world':''
                    }
    
    df['region'] = df['variable'].map(region_mapper)
    df['type'] = df['variable'].map(type_mapper)

    to_append = df.copy()
    to_append = to_append[to_append.variable == u'world']
    to_append.variable, to_append.region, to_append['%'] = '', '', 0

    df = pd.concat([to_append, df])

    df['value'] = df['%'] * df[u'world_gdp_billions_2012_ppp']
    df.dropna(subset=['value'], inplace=True)

    to_melt = ['%', 'value']
    to_keep = [x for x in df.columns if x not in to_melt]

    df = pd.melt(df, id_vars = to_keep, value_vars = to_melt, var_name = 'type_value')
    df['date_year'], _ = df.date.str.split('-',1).str

    return df

def prepare_income(df):

    CLEAN_COUNTRIES = {
        'australia':'Australie',
        'canada':'Canada',
        'europe':'Europe',
        'france':'France',
        'germany':'Allemagne',
        'italy':'Italie',
        'japan':'Japon',
        'spain':'Espagne',
        'u_s':'Etats Unis',
        'u_k':'GB'
    }
    
    df.rename(columns=CLEAN_COUNTRIES, inplace=True)
    to_keep = ['year','median']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df['median'] = df.median(axis=1)
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt)
    df['date_year'], _ = df.year.str.split('-',1).str


    return df

def prepare_employemnt(df):
    to_keep = ['year']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt)
    df['country'], df['sector'] = df.variable.str.split('_',1).str

    return df

def prepare_labor(df):
    to_keep = ['year']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt)
    
    VAR_DIC = {
        'capital_share':'Part du Capital dans le Revenu National',
        'labour_share':'Part du Travail dans le Revenu National',
    };

    df.variable = df.variable.replace(VAR_DIC)
    df['year_text']= df['year'].copy()
    return df
    

def augment(dfs):
    """
    Insert here code to augment your data frames during preprocessing
    """
    dfs['growth-vs-return'] = prepare_growth(dfs['growth-vs-return'])
    dfs['concentration-of-wealth'] = prepare_concentration(dfs['concentration-of-wealth'])
    dfs['world-output-distribution'] = prepare_output(dfs['world-output-distribution'])
    dfs['private-capital-vs-national-income'] = prepare_income(dfs['private-capital-vs-national-income'])
    dfs['employment-by-sector'] = prepare_employemnt(dfs['employment-by-sector'])
    dfs['labor-vs-capital'] = prepare_labor(dfs['labor-vs-capital'])

    # Add domain to each dataframe
    for domain, df in dfs.items():
        df['domain'] = domain

    # Example calcuation that will only be done if the data or function code has changed
    # dfs['domain_c'] = compute_domain_c(dfs['domain_a'], dfs['domain_b'])


    return dfs
