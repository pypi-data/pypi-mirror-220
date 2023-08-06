# -*- coding: utf-8 -*-
"""
This is a unit test for Analisis class.

Created on Thu Jul 13 11:54:41 2023 

@author: Bruk
"""
import pandas as pd
from analysis import Analyser


def test_calculate_inflation():
    inf_analyser = Analyser()
    
    cpi_data = pd.DataFrame.from_dict({
    '': ['Ethiopia'],
    'Dec_2019': [157.86],
    'Jan_2020': [158.72],
    'Feb_2020': [164.53],
    'Mar_2020': [170.44],
    'Apr_2020': [175.2]
    }).set_index('')
    
    expected_inflation_result = pd.DataFrame.from_dict({
    '': ['Ethiopia'],
    'Jan_2020_INF': [0.5],
    'Feb_2020_INF': [3.7],
    'Mar_2020_INF': [3.6],
    'Apr_2020_INF': [2.8]
    }).set_index('')
    
    actual_result = inf_analyser.inflation_calculator(cpi_data)
    assert actual_result.equals(expected_inflation_result)
    
    
def test_get_all_products_of_a_country():
    inf_analyser = Analyser()
    expected_inflation_result = {
            #'Dec_2019_INF': [32.1,60.5,0.1,34.4,57.9,31.2,58.7,41.4,40.1,55.1,40.6], Reference Month
            'Jan_2020_INF': [-3.5,1.4,-0.8,2.8,0.5,-5.0,2.4,1.7,3.3,0.0,2.2],
            'Feb_2020_INF': [3.9,-4.3,1.8,-3.9,3.7,4.3,4.3,1.0,-1.0,1.3,2.4],
            'Mar_2020_INF': [15.1,3.2,1.3,-0.5,3.6,4.5,-0.1,1.5,-1.3,0.5,1.1],
            'Apr_2020_INF': [4.1,0.8,1.4,2.0,2.8,2.2,-0.4,0.5,-0.4,0.0,11.8]}
			

    expected_result = pd.DataFrame(expected_inflation_result, index=[
                                    'Alcoholic_Beverages',
                                   'Clothing',
                                   'Communication',
                                   'Education',
                                   'Food',
                                   'Health',
                                   'Housing_Energy',
                                   'Misc_Goods_Services',
                                   'Recreation_Culture',
                                   'Restaurants_Hotels',
                                   'Transport',])

    actual_result = inf_analyser.all_products_inflation('Ethiopia','Dec_2019','May_2020') 
    assert actual_result.equals(expected_result)


