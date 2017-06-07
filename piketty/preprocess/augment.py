# coding: utf-8
from __future__ import unicode_literals

import pandas as pd

from app.etl.cache import cache


@cache()
def compute_domain_c(domain_a, domain_b):
    # [do some heavy and slow computation]
    domain_c = domain_a + domain_b
    return domain_c

def prepare_concentration(df):

    to_melt = [x for x in df.columns if x != 'date']
    df = pd.melt(df, id_vars='date', value_vars = to_melt)
    df['zone'], df['type'] = df.variable.str.split('_',1).str

    return df

def prepare_output(df):

    to_keep = ['date',u'world_gdp_billions_2012_ppp']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt, value_name='%')
    df = df[df.variable != 'total']

    region_mapper = {
                        u'africa':'Africa', u'america':'America', u'asia':'Asia', u'australia_nz':'Asia', u'central_asia':'Asia',
                        u'china':'Asia', u'eastern_europe':'Europe', u'europe':'Europe', u'india':'Asia', u'japan':'Japan',
                        u'latin_america':'America', u'middle_east_y_c_turkey':'Asia', u'north_america':'America',
                        u'northern_africa':'Africa', u'other_asian_countries':'Asia',
                        u'russia_ukraine_belarus_moldavia':'Europe', u'sub_saharan_africa':'Africa',
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

    return df

def prepare_income(df):
    to_keep = ['year','median']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df['median'] = df.median(axis=1)
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt)

    return df

def prepare_employemnt(df):
    to_keep = ['year']
    to_melt = [x for x in df.columns if x not in to_keep]
    
    df = pd.melt(df, id_vars=to_keep, value_vars = to_melt)
    df['country'], df['sector'] = df.variable.str.split('_',1).str

    return df
    

def augment(dfs):
    """
    Insert here code to augment your data frames during preprocessing
    """

    dfs['concentration-of-wealth'] = prepare_concentration(dfs['concentration-of-wealth'])
    dfs['world-output-distribution'] = prepare_output(dfs['world-output-distribution'])
    dfs['private-capital-vs-national-income'] = prepare_income(dfs['private-capital-vs-national-income'])
    dfs['employment-by-sector'] = prepare_employemnt(dfs['employment-by-sector'])

    # Add domain to each dataframe
    for domain, df in dfs.iteritems():
        df['domain'] = domain

    # Example calcuation that will only be done if the data or function code has changed
    # dfs['domain_c'] = compute_domain_c(dfs['domain_a'], dfs['domain_b'])


    return dfs
