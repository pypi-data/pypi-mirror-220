#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 20:26:49 2023

@author: alejandracamelocruz
"""

import pandas as pd
from preprocessor import Preprocessor
import os

prpr = Preprocessor()

cwd = os.getcwd()
data_dir = os.path.abspath(os.path.join(cwd, os.pardir, 'data'))

def test_product():
    
    correct_product_list = set(['Alcoholic_Beverages', 'Clothing', 'Communication',
                               'Education', 'Food', 'Health', 'Housing_Energy', 'Misc_Goods_Services',
                               'Recreation_Culture', 'Restaurants_Hotels', 'Transport'])

    test_product_list = set(prpr.list_products())

    assert correct_product_list == test_product_list


def test_get_cpi_data_by_product():
    expected_result=(157,281)
    actual_result = prpr.by_product('Education')
    assert actual_result.shape == expected_result


def test_get_countries_cpi_data_by_year():
    expected_cpi_result = pd.DataFrame.from_dict({
    '': ['France','Germany'],
    'Jan_2022': [110.41,106.50],
    'Feb_2022': [110.82,107.60],
    'Mar_2022': [111.87,108.50],
    'Apr_2022': [113.61,112.00],
    'May_2022': [114.75,114.00]
    }).set_index('')
    
    actual_result = prpr.by_year('Food',['France','Germany'], 'Jan_2022', 'Jun_2022')
    assert actual_result.equals(expected_cpi_result)
    
    
def test_get_cpi_data_by_country():
    expected_cpi_result_shape = (3,281)
    actual_result = prpr.by_country('Education',['France','Ethiopia','Germany'])
    assert actual_result.shape == expected_cpi_result_shape
    

    



   				