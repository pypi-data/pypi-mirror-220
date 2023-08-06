#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This Analysis class calculates inflation rate of based on the preprocessed data, 
and also analyzes all products inflation rate of a country.  

Copyright (C) 2023

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

contact email: tsega@uni-potsdam.de, camelocruz@uni-potsdam.de, kar@uni-potsdam.de, leon.oparin@uni-potsdam.de

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

contact email: tsega@uni-potsdam.de, camelocruz@uni-potsdam.de, 
                kar@uni-potsdam.de, leon.oparin@uni-potsdam.de
@author: Bruk Asrat

"""

import argparse
import pandas as pd
from preprocessor import Preprocessor

class Analyser(Preprocessor):
    """
    Class Analyser calculates inflation rate and analyzes all products inflation
    rate of a country.
    """
    def set_datafile(self,product:str,country_list:list,start_time:str,
                     stop_time:str) -> pd.DataFrame:
        """
        Data setter for the Analyzer class.

        Parameters
        ----------
        product : str
            A list of products.
        country_list : list
            A list of countries.
        start_time : str
            The first month or reference date to calculate inflation rate.
        stop_time : str
            The last month of the date range.

        Returns
        -------
        TYPE
            Return a dataframe.

        """
        self.product = product
        self.country_list = country_list
        self.start_time = start_time
        self.stop_time = stop_time
        self.data = self.by_year(product,country_list,start_time,stop_time)

        return self.data


    def inflation_calculator(self,input_df:pd.DataFrame) -> pd.DataFrame:
        """
        This function calculates inflation rate of a given dataframe.

        Parameters
        ----------
        input_df : pandas DataFrame
            well formulated dataframe result of other functions ready to be analysed. 

        Returns
        -------
        inflation_result : dataframe
            returns calculated inflation rate

        """
        prev_cpi = 100
        time_span = input_df.columns.values.tolist()
        for time in time_span:
            infl = time + '_INF'
            #Inflation = ((New CPI - Previous Month CPI)/ Previous Month CPI) X 100
            val = round(((input_df[time]-prev_cpi) / prev_cpi)* 100 , 1)
            prev_cpi = input_df[str(time)]
            input_df[infl] = val

        inflation_result = input_df.loc[:, ~input_df.columns.isin(time_span)]
        inflation_result = inflation_result.iloc[:,1:]

        return inflation_result


    def all_products_inflation(self,nation:str,start_time:str,stop_time:str) -> pd.DataFrame:
        """
        This function merge all products inflation rate of a given country for 
        specific period of time, provided by the user.

        Parameters
        ----------
        nation : string
            The name of the country
        start : string
            The initial month or the reference month.
        stop : string
            The last month of the time.

        Returns
        -------
        resultframe : dataframe
        Returns a dataframe of all products for a given period of time and country.

        """
        product_list = self.list_products()
        l_nation = [nation]
        resultframe = pd.DataFrame()

        for product in product_list:             
            result = self.set_datafile(product,l_nation,start_time,stop_time)
            resultframe = resultframe.append(result,ignore_index=True,sort=False)

        for i,product in enumerate(product_list):                
            resultframe = resultframe.rename(index={i: product_list[i]})

        products_inf = self.inflation_calculator(resultframe)

        return products_inf


def main(args):
    """
    The main entry function from command line interface.

    Parameters
    ----------
    args : TYPE
        Accepts arguments product,country list, period of time from command line.

    Returns
    -------
    None.

    """
    analyser = Analyser()

    args = parser.parse_args()

    if not args.product or args.product is None:
        print("Missing arguement : --product is required")
        print(analyser.list_products())
    else:
        if not args.countries or args.countries is None:
            analyser.by_product(args.product)
            print("Missing arguement : --countries is required")
            print(analyser.list_countries())
        else:
            if not args.time:
                analyser.by_country(args.product,args.countries)
                print("Missing arguement : --time is required")
                print(analyser.list_years())
            else:
                start,stop = args.time
                data = analyser.by_year(args.product,args.countries,start,stop)
                print(data)


if __name__ == "__main__":
    analyser = Analyser()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--product', type=str, help='Product name')
    parser.add_argument('-c', '--countries', nargs='+', help='List of countries')
    parser.add_argument('-t', '--time', type=str, nargs=2, help='Start, Stop')

    args = parser.parse_args()

    if not args.product or args.product is None:
        print("Missing arguement : --product is required")
        print(analyser.list_products())
    else:
        if not args.countries or args.countries is None:
            analyser.by_product(args.product)
            print("Missing arguement : --countries is required")
            print(analyser.list_countries())
        else:
            if not args.time:
                analyser.by_country(args.product,args.countries)
                print("Missing arguement : --time is required")
                print(analyser.list_years())
            else:
                start,stop = args.time
                data = analyser.set_datafile(args.product,args.countries,start,stop)
