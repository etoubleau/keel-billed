# coding: utf-8

# import pandas as pd
# import pdb
# from lib import datagenerator
# import os


outputs = {
    'lines1': {
        'input_domains': ['lines1'],
        'function_name': 'out_lines1'
    },
    'lines2': {
        'input_domains': ['lines2', 'lines1'],
        'function_name': 'out_lines2'
    },
    'dashboards': {
        'input_domains': ['dashboards'],
        'function_name': 'same'
    },
    'market-breakdown': {
        'input_domains': ['market-breakdown'],
        'function_name': 'same'
    },
    'gsheets': {
        'input_domains': ['gsheets'],
        'function_name': 'same'
    },
    'ranks': {
        'input_domains': ['ranks'],
        'function_name': 'same'
    },
    'dynamic_barlinechart': {
        'input_domains': ['dynamic_barlinechart'],
        'function_name': 'same'
    },
    'funnelchart': {
        'input_domains': ['funnelchart'],
        'function_name': 'same'
    },
    'free_text_home': {
        'input_domains': ['free_text_home'],
        'function_name': 'same'
    },
    'scorecard_home': {
        'input_domains': ['scorecard_home'],
        'function_name': 'same'
    },
    'bubble_bissector': {
        'input_domains': ['bubble_bissector'],
        'function_name': 'same'
    },
    'heatmap_home': {
        'input_domains': ['heatmap_home'],
        'function_name': 'same'
    },
    'leaderboard_centered_avg': {
        'input_domains': ['leaderboard_centered_avg'],
        'function_name': 'same'
    },
    'slave_heatmap': {
        'input_domains': ['slave_heatmap'],
        'function_name': 'same'
    },
    'heatmap': {
        'input_domains': ['heatmap'],
        'function_name': 'same'
    },
    'books': {
        'input_domains': ['books'],
        'function_name': 'same'
    },
    '0_36200': {
        'input_domains': ['0_36200'],
        'function_name': 'same'
    },
    '0_36202': {
        'input_domains': ['0_36202'],
        'function_name': 'same'
    },
    '0_37100': {
        'input_domains': ['0_37100'],
        'function_name': 'same'
    },
    '0_37101': {
        'input_domains': ['0_37101'],
        'function_name': 'same'
    },
    '0_32101': {
        'input_domains': ['0_32101'],
        'function_name': 'same'
    },
    '0_30201': {
        'input_domains': ['0_30201'],
        'function_name': 'same'
    },
    '0_30202': {
        'input_domains': ['0_30202'],
        'function_name': 'same'
    },
    '0_30203': {
        'input_domains': ['0_30203'],
        'function_name': 'same'
    },
    '0_32205_0': {
        'input_domains': ['0_32205_0'],
        'function_name': 'same'
    },
    '0_32205_1': {
        'input_domains': ['0_32205_1'],
        'function_name': 'same'
    },
    '0_32206_0': {
        'input_domains': ['0_32206_0'],
        'function_name': 'same'
    },
    '0_32206_1': {
        'input_domains': ['0_32206_1'],
        'function_name': 'same'
    },
    '0_32104': {
        'input_domains': ['0_32104'],
        'function_name': 'same'
    },
    '0_32105': {
        'input_domains': ['0_32105'],
        'function_name': 'same'
    },
    '0_32106': {
        'input_domains': ['0_32106'],
        'function_name': 'same'
    },
    '0_32107': {
        'input_domains': ['0_32107'],
        'function_name': 'same'
    },
    '0_30204': {
        'input_domains': ['0_30204'],
        'function_name': 'same'
    },
    '0_32100': {
        'input_domains': ['0_32100'],
        'function_name': 'same'
    },
    '0_32102': {
        'input_domains': ['0_32102'],
        'function_name': 'same'
    },
    '0_34201': {
        'input_domains': ['0_34201'],
        'function_name': 'same'
    },
    '0_34204': {
        'input_domains': ['0_34204'],
        'function_name': 'same'
    },
    '0_34200': {
        'input_domains': ['0_34200'],
        'function_name': 'same'
    },
    '0_37102': {
        'input_domains': ['0_37102'],
        'function_name': 'same'
    },
    '0_30205': {
        'input_domains': ['0_30205'],
        'function_name': 'same'
    },
    '0_40206': {
        'input_domains': ['0_40206'],
        'function_name': 'same'
    },
    '0_201_1': {
        'input_domains': ['0_201_1'],
        'function_name': 'same'
    },
    '0_201_1_avg': {
        'input_domains': ['0_201_1_avg'],
        'function_name': 'same'
    },
    'timeline': {
        'input_domains': ['timeline'],
        'function_name': 'same'
    },
    'horizontal_barchart_groups': {
        'input_domains': ['horizontal_barchart_groups'],
        'function_name': 'same'
    },
    'horizontal_barchart_evolution': {
        'input_domains': ['horizontal_barchart_evolution'],
        'function_name': 'same'
    },
    'horizontal_barchart_sparklines': {
        'input_domains': ['horizontal_barchart_sparklines'],
        'function_name': 'same'
    },
    'horizontal_barchart_legacy_sparklines': {
        'input_domains': ['horizontal_barchart_legacy_sparklines'],
        'function_name': 'same'
    },
    # 'horizontal_barchart_simple': {
    #     'input_domains': ['horizontal_barchart_simple'],
    #     'function_name': 'same'
    # },
    'waterfall_new': {
        'input_domains': ['waterfall_new'],
        'function_name': 'same'
    },
    'waterfall_new_categorized': {
        'input_domains': ['waterfall_new_categorized'],
        'function_name': 'same'
    },
    'cities_data': {
        'input_domains': ['cities_data'],
        'function_name': 'same'
    },
    'france_regions': {
        'input_domains': ['france_regions'],
        'function_name': 'same'
    },
    'barlines_bars': {
        'input_domains': ['barlines_bars'],
        'function_name': 'same'
    },
    'barlines_lines': {
        'input_domains': ['barlines_lines'],
        'function_name': 'same'
    },
    'barlines_bars_filter': {
        'input_domains': ['barlines_bars_filter'],
        'function_name': 'same'
    },
}

update_outputs = {
    'dynamic_out_lines': {
        'input_domains': [],
        'function_name': 'dynamic_out_lines'
    }
}


def dynamic_out_lines(dfs, output_domain):
    return {
        'out_lines3': {
            'input_domains': ['lines1'],
            'function_name': 'out_lines3'
        },
        'out_lines4': {
            'input_domains': ['lines2'],
            'function_name': 'out_lines4'
        },
    }


def same(dfs, output_domain):
    return dfs[output_domain]


def out_lines1(dfs, output_domain):
    return {'aa': dfs['lines1']}


def out_lines2(dfs, output_domain):
    return {
        'aaa': dfs['lines2'],
        'bbb': dfs['lines1']
    }


def out_lines3(dfs, output_domain):
    return {
        'zzzz': dfs['lines1']
    }


def out_lines4(dfs, output_domain):
    return {
        'ygtd': dfs['lines2'],
    }


def augment(dfs):
    """
    Insert here code to augment your data frames during preprocessing
    """

    # Add domain to each dataframe
    for domain, df in dfs.items():
        df['domain'] = domain

    # file_path = os.path.dirname(os.path.abspath(__file__))
    # small_app_id = os.path.basename(os.path.abspath(os.path.join(file_path, os.pardir)))
    # generator = datagenerator.builder(small_app_id)

    # ### Example
    # labels = {
    #     'Par Zone': ['Calvaldos','Loire Atlantique','Isère','Alpes Maritime',
    #                  'Picardie','Manche','Orne','Mozelle'],
    #     'Par PDV': ['Caen','Rennes','Nantes','Lyon','Lille']
    #     }
    # categories = ['Toutes zones rangées','Au moins 1 zone pas propre','Toutes zones sales']
    # breakdown = ['Par Zone','Par PDV']
    # generator( {'stack':True}, labels, categories, breakdown, 'test_generator')

    return dfs
