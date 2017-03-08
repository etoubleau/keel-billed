# coding=utf-8
"""
Demo augment.py

The goal here is to give a concrete example on pandas method and decorators
and utility functions from Laputa. Its purpose is also to give some good
practices regarding function naming and how to arrange your code.

You will find here some functions, that take one ore more DataFrames and that
can be sorted into three categories:

1. cleaning and simple reshaping, aggregation (mostly cleaning here)
2. intermediate computation methods
3. output functions that does some transformation to result of the previous
functions.

There are two input domains and five output for this demo augment.py. The five
outputs can be grouped into to categories: medals and feminization. You will
two paths of functions, one for each.

The (visible, see below) pandas functions used are:

* merge
* drop
* rename
* pivot_table
* pct_change

Other pandas are used, but are hidden inside some of Laputa's utility
functions like:

* roll_up

There are also decorators that you should use in order to focus on your
aggregation, reshaping, cleaning, etc. and not worry about exceptions and
logging. There can also be extremely useful to have a quick idea of what is
happening with a quick at the logs. These decorators are:

* log_time
* log_message
* log_shapes

"""

import pandas as pd
from app.etl import util
from app.etl.decorators import log_time, log_message, log_shapes
from app.log import Logger

# TODO: explain (why AM_..., IOC_..., what are these)

# Global variables
# All of the following variables are column names. The naming convention is:
# a prefix to identify the data source and a name for the column (the same as
# the real one since they are quite short and easy to understand).
# The two data sources are the All medalists and IOC Country codes sheets (
# from the same Google spreadsheet document), the prefixes are: AM and IOC.
# The goal is first to give an idea of the columns and therefore the kind of
# data that will be found, and then to avoid too many hardcoded strings inside
# the code: if a column name changes, just change the value of the global
# variable.

AM_EDITION = 'Edition'
AM_COUNTRY_CODE = 'NOC'
AM_COUNTRY = 'Country'

AM_SPORT = 'Sport'
AM_DISCIPLINE = 'Discipline'
AM_EVENT = 'Event'

AM_MEDAL = 'Medal'
AM_GOLD = 'Gold'
AM_SILVER = 'Silver'
AM_BRONZE = 'Bronze'
AM_TOTAL = 'Total'

AM_GENDER = 'Gender'
AM_MEN = 'Men'
AM_WOMEN = 'Women'
AM_ATHLETE = 'Athlete'
AM_TOTAL_ATHLETES = 'Total_athletes'
AM_PERCENTAGE_WOMEN = 'Percentage_women'
AM_EVOLUTION_WOMEN = 'Evolution_women'
AM_EVOLUTION_PERCENTAGE_WOMEN = 'Evolution_percentage_women'

IOC_ISO_CODE = 'ISO code'
IOC_COUNTRY1 = 'Country.1'
IOC_COUNTRY = 'Country'
IOC_IOCC = 'Int Olympic Committee code'

logger = Logger(__name__)


def augment(dfs):
    """
    Insert here code to augment your data frames during preprocessing
    """

    df = dfs['AM']
    country_codes = dfs['IOC']

    # ----- Medals ----- #

    # Clean up (step 1)
    country_codes = clean_country_codes(country_codes)

    # Medals by edition and by sports (step 2)
    df_sports = compute_medals_sports(df)

    # Medals by edition and by country (step 2)
    df_country = compute_medals_country(df, country_codes)

    # Re-ordering and sort for debug and the small app. (step 3)
    medals = compute_out_medals(df_sports, df_country)
    dfs['medals_sports'] = medals['sports']
    dfs['medals_country'] = medals['country']

    # ----- Feminization ----- #
    # Step 1 already done (clean country codes)

    # Feminization by edition (step 2)
    df_all = compute_feminization(df, [AM_EDITION])

    # Feminization by edition and by sport (step 2)
    df_sports = compute_feminization(df, [AM_EDITION, AM_SPORT])

    # Feminization by edition and by country (step 2)
    df_country = compute_feminization(df, [AM_EDITION, AM_COUNTRY_CODE])

    # Feminization by edition, country and sport (step 2)
    df_sports_country = compute_feminization(df, [AM_EDITION, AM_SPORT, AM_COUNTRY_CODE])

    # Re-order and merges (step 3)
    feminization = compute_out_feminization(df_all=df_all, df_sports=df_sports,
                                            df_country=df_country, df_sports_country=df_sports_country,
                                            country_codes=country_codes)
    dfs['feminization_all'] = feminization['all']
    dfs['feminization_sports'] = feminization['sports']
    dfs['feminization_country'] = feminization['country']
    dfs['feminization_sports_country'] = feminization['sports_country']

    del dfs['AM']
    del dfs['IOC']

    return dfs


def clean_country_codes(country_codes):
    """
    Drop two unnecessary columns and rename the two remaining
    Args:
        country_codes (DataFrame): Country codes with their full names

    Returns:
        DataFrame: cleaned country codes with two columns: code and name

    """
    codes = country_codes.drop([IOC_ISO_CODE, IOC_COUNTRY1], axis=1)
    return codes.rename(columns={IOC_IOCC: AM_COUNTRY_CODE, IOC_COUNTRY: AM_COUNTRY})


@log_time(logger)
@log_message(logger, "Medals output ready")
def compute_out_medals(df_sports, df_country):
    """
    Compute medals (total, gold, silver, bronze) by sports and country (two
    different DataFrames). The computation is done inside other methods. This
    is mostly for reordering and renaming.

    Args:
        df (DataFrame): Information to extract
        country_codes (DataFrame): Full name and country codes.

    Returns:
        dict: two keys: sports and country

    """

    # Medals by edition and by sports
    df_sports = df_sports[[AM_EDITION, 'Type', 'Name', AM_TOTAL, AM_GOLD, AM_SILVER,
                                 AM_BRONZE, AM_SPORT, AM_DISCIPLINE, AM_EVENT]]

    # Medals by edition and by country
    df_country.columns = [AM_COUNTRY, AM_COUNTRY_CODE] + df_country.columns.tolist()[2:]
    df_country = df_country[[AM_EDITION, AM_COUNTRY, AM_COUNTRY_CODE, AM_TOTAL, AM_GOLD, AM_SILVER, AM_BRONZE]]
    df_country = df_country.sort_values('Edition')

    return {'sports': df_sports, 'country': df_country}


def compute_medals(df_medals, group):
    """
    Compute number of gold, silver and bronze medals and the total.

    Args:
        df (DataFrame): Extract information from it
        group (list): List of column names to group by (pandas groupby)

    Returns:
        DataFrame: Total, gold, silver and bronze medals by edition, sport,
            etc. (columns inside the group argument).

    """
    total_medals = df_medals.groupby(group)[AM_MEDAL].count()
    total_gold = df_medals[df_medals[AM_MEDAL] == AM_GOLD].groupby(group)[AM_MEDAL].count()
    total_silver = df_medals[df_medals[AM_MEDAL] == AM_SILVER].groupby(group)[AM_MEDAL].count()
    total_bronze = df_medals[df_medals[AM_MEDAL] == AM_BRONZE].groupby(group)[AM_MEDAL].count()

    total_medals = pd.DataFrame(total_medals).reset_index()
    total_gold = pd.DataFrame(total_gold).reset_index()
    total_silver = pd.DataFrame(total_silver).reset_index()
    total_bronze = pd.DataFrame(total_bronze).reset_index()

    totalgold = pd.merge(total_medals,
                         total_gold,
                         on=group,
                         how='inner',
                         suffixes=('_Total', '_Gold'))
    silverbronze = pd.merge(total_silver,
                            total_bronze,
                            on=group,
                            how='inner',
                            suffixes=('_Silver', '_Bronze'))
    df_medals = pd.merge(totalgold, silverbronze, on=group, how='inner')
    return df_medals.rename(columns={
        AM_MEDAL + '_Total': 'Total',
        AM_MEDAL + '_Gold': 'Gold',
        AM_MEDAL + '_Silver': 'Silver',
        AM_MEDAL + '_Bronze': 'Bronze',
    })


@log_time(logger)
@log_shapes(logger)
def compute_medals_country(df, country_codes):
    """
    Compute medals by country, add country codes, rename columns.
    Args:
        df (DataFrame): Information to extract
        country_codes (DataFrame): Country full names and codes

    Returns:
        DataFrame: Medals per country (per edition)

    """
    # Medals
    group = [AM_COUNTRY_CODE, AM_EDITION]
    total_medals = compute_medals(df, group)
    total_medals.columns = [AM_COUNTRY_CODE, AM_EDITION, AM_TOTAL, AM_GOLD, AM_SILVER, AM_BRONZE]

    # Add country Codes
    return pd.merge(country_codes, total_medals, on=AM_COUNTRY_CODE, how='inner')


@log_time(logger)
@log_shapes(logger)
def compute_medals_sports(df):
    """
    Compute medals by sports and by edition. Keep the hierarchy information:
    Event inside Discipline and Discipline inside Sport.

    Args:
        df (DataFrame): Information to extract

    Returns:
        DataFrame: Medals per sports, discipline and event (per edition)

    """
    # Medals
    group = [AM_EDITION, AM_SPORT, AM_DISCIPLINE, AM_EVENT]
    total_medals = compute_medals(df, group)

    total_medals = util.roll_up(total_medals,
                                levels=[AM_SPORT, AM_DISCIPLINE, AM_EVENT],
                                groupby_vars=[AM_TOTAL, AM_GOLD, AM_SILVER, AM_BRONZE],
                                extra_groupby_cols=[AM_EDITION],
                                var_name='Type',
                                value_name='Name')
    return total_medals


@log_time(logger)
@log_message(logger, "Feminization output ready")
def compute_out_feminization(df_all, df_sports, df_country, df_sports_country, country_codes):
    """
    Compute feminization rate by edition: globaly, by sports, by country and
     by sports and country. With evolution.

    Args:
        df_all (DataFrame): Feminization by editon
        df_sports (DataFrame): Feminization by sports
        df_country (DataFrame): Feminization by country
        df_sports_country (DataFrame): Feminization by sports and country
        country_codes (DataFrame): Full name and country codes.

    Returns:
        dict: Four keys: all, sports, country, sports_country

    """

    df_all = df_all[
        [AM_EDITION, AM_MEN, AM_WOMEN, AM_TOTAL_ATHLETES,
         AM_PERCENTAGE_WOMEN, AM_EVOLUTION_WOMEN, AM_EVOLUTION_PERCENTAGE_WOMEN]
    ]

    df_sports = df_sports[
        [AM_EDITION, AM_SPORT, AM_MEN, AM_WOMEN, AM_TOTAL_ATHLETES,
         AM_PERCENTAGE_WOMEN, AM_EVOLUTION_WOMEN, AM_EVOLUTION_PERCENTAGE_WOMEN]
    ]

    df_country = pd.merge(df_country, country_codes, on=AM_COUNTRY_CODE, how='inner')
    df_country = df_country[
        [AM_EDITION, AM_COUNTRY_CODE, AM_COUNTRY, AM_MEN, AM_WOMEN, AM_TOTAL_ATHLETES,
         AM_PERCENTAGE_WOMEN, AM_EVOLUTION_WOMEN, AM_EVOLUTION_PERCENTAGE_WOMEN]
    ]

    df_sports_country = pd.merge(df_sports_country, country_codes, on=AM_COUNTRY_CODE, how='inner')
    df_sports_country= df_sports_country[
        [AM_EDITION, AM_COUNTRY_CODE, AM_COUNTRY, AM_SPORT, AM_MEN, AM_WOMEN, AM_TOTAL_ATHLETES,
         AM_PERCENTAGE_WOMEN, AM_EVOLUTION_WOMEN, AM_EVOLUTION_PERCENTAGE_WOMEN]
    ]

    return {'all':df_all, 'sports': df_sports, 'country': df_country, 'sports_country': df_sports_country}


@log_time(logger)
@log_shapes(logger)
def compute_feminization(df, index_cols):
    """
    Compute feminization rate for some given variables (index_cols).
    Computations are: total of athletes, percentage of women, evolution of the
    number of women, the evolution of the percentage of women.

    Args:
        df (DataFrame): Information DataFrame
        index_cols (list): pandas pivot_table index columns (columns that will
            become indexes)

    Returns:
        DataFrame: Reshaped DataFrame with extra information.

    """
    df_fem = pd.pivot_table(df,
                            index=index_cols,
                            columns=AM_GENDER,
                            values=AM_ATHLETE,
                            aggfunc=pd.DataFrame.count)
    df_fem = df_fem.reset_index().fillna(0)
    df_fem[AM_TOTAL_ATHLETES] = df_fem[AM_WOMEN] + df_fem[AM_MEN]
    df_fem[AM_PERCENTAGE_WOMEN] = (df_fem[AM_WOMEN] / df_fem[AM_TOTAL_ATHLETES]) * 100
    df_fem[AM_EVOLUTION_WOMEN] = df_fem[AM_WOMEN].pct_change() * 100
    df_fem[AM_EVOLUTION_PERCENTAGE_WOMEN] = df_fem[AM_PERCENTAGE_WOMEN].pct_change() * 100
    df_fem.columns.name = ''

    return df_fem


if __name__ == '__main__':
    import os

    data_sources_base_dir = 'small_apps/standardized/data_sources'
    all_medalists = pd.read_csv(os.path.join(data_sources_base_dir, 'all_medalists.csv'), skiprows=4)
    ioc_codes = pd.read_csv(os.path.join(data_sources_base_dir, 'ioc_codes.csv'))
    dfs = {'AM': all_medalists, 'IOC': ioc_codes}
    dfs = augment(dfs)
