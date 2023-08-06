#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This Preprocessor class provides cleaning and filetring of the data provided 
in the data folder under root folder


Copyright (C) 2023 Kshitij Kar, Alejandra Camelo Cruz

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

contact email: camelocruz@uni-potsdam.de, kar@uni-potsdam.de

"""
import os
import argparse
import logging
import pandas as pd
import numpy as np


class Preprocessor:
    '''Preprocessor for data cleaning and data filtering'''

    def __init__(self):
        self.data_folder = self._get_relative_data_directory()
        self.files = [os.path.join(self.data_folder, file)
                      for file in os.listdir(self.data_folder)]
        self.product = "Education"
        self.cl = ['Austria',
                    'Belgium',
                    'Bulgaria',
                    'Croatia',
                    'Czech_rep.',
                    'Denmark',
                    'Estonia',
                    'Finland',
                    'France',
                    'Germany',
                    'Greece',
                    'Hungary',
                    'Iceland',
                    'Ireland',
                    'Italy',
                    'Latvia',
                    'Lithuania',
                    'Luxembourg',
                    'Montenegro',
                    'Netherlands',
                    'Norway',
                    'Poland',
                    'Portugal',
                    'Russian_federation',
                    'Serbia',
                    'Spain',
                    'Switzerland',
                    'Ukraine',
                    'United_kingdom']


    def _index_cleaning(self, index_list:list) -> list:
        '''
        This function takes the index list of any DataFrame, cleans it 
        and returns it to the calling function to replace the previous 
        data index with the cleaned data index. 

        Parameters
        ----------
        index_list : list
            list with DataFrame indexes.

        Returns
        -------
        list
            index list with clean strings.

        '''
        outlist = []
        for country in index_list:
            country = country.capitalize()
            if country[0:5] == "China":
                outlist.append(country.split(": ")[-1].replace(" ","_"))
            else:
                outlist.append(country.split(",")[0].replace(" ","_"))

        return outlist


    def _data_cleaning(self, file_location:str) -> pd.DataFrame:
        '''
        This function reads any particular data set provided and 
        cleans the column headers and indexes and returns the clened DataFrame.

        Parameters
        ----------
        file_location : str
            path to the data file to be cleaned.

        Returns
        -------
        data : Pandas DataFrame
            Pandas DataFrame with clean columns and rows.

        '''
        if file_location.endswith(".xlsx"):
            data = pd.read_excel(file_location)
        elif file_location.endswith(".csv"):
            data = pd.read_csv(file_location)
        data.index = data["Unnamed: 0"]
        data = data.drop(columns=["Unnamed: 0"])
        data.columns = [c.strip().replace(" ","_") for c in data.columns.values.tolist()]
        data.index = self._index_cleaning(data.index.tolist())

        return data


    def list_products(self) -> list:
        '''
        List products available in a data file

        Returns
        -------
        list
            list with possible product entries.

        '''
        list_products = []
        for file in self.files:
            if file.endswith(".xlsx"):
                list_products.append(file.split("_CPI_")[-1].split(".")[0])
            else:
                continue
        return list_products


    def by_product(self, product:str) -> pd.DataFrame:
        '''
        This function asks the user to input the product they wish to analyse 
        and returns the data set with only that product.

        Parameters
        ----------
        product : TYPE
            DESCRIPTION.

        Returns
        -------
        data : TYPE
            DESCRIPTION.

        '''
        self.product = product
        if product == "" or product is None:
            print("No product provided. Here are your options :")
            print(self.list_products())

        else:
            logging.basicConfig(level=logging.INFO)
            logging.info(bcolors.OKGREEN + f"You have chosen {product}"+
                bcolors.ENDC)
            if product in self.list_products():
                self.data_file = os.path.abspath(
                    os.path.join(self.data_folder, f"Consumer_Price_Index_CPI_{product}.xlsx"))
                data = self._data_cleaning(self.data_file)

                return data

            else:
                logging.basicConfig(level=logging.INFO)
                logging.info(bcolors.WARNING + f"{product} is not a valid option."+
                bcolors.ENDC)
                print(self.list_products())


    def list_countries(self, intext="") -> list:
        '''
        List all the countries available in a data file
        
        Parameters
        ----------
        intext : TYPE, optional
            return list of countries matching intext string. The default is "".

        Returns
        -------
        List
            list with specified countries. If nothing or all is given, it returns 
            all the countries.

        '''
        continent_list = ["Africa","Asia","Europe","North_america","Oceania","South_america"]
        data = self._data_cleaning(self.files[0])
        list_countries = data.index.to_list()
        # if intext != "all" or intext is None:
        #     intext = input("Enter a part of the countries you want. "
        #                 "Don't write anything or write \"all\" if you want to see "
        #                 "a list with all available countries: ")
        # else:
        #     pass

        intext = intext.capitalize()
        all_countries = (intext == "" or intext == 'All')

        if all_countries:
            logging.basicConfig(level=logging.INFO)
            logging.info(bcolors.HEADER + f"Additional options for regions :"+
              bcolors.ENDC)
            print(continent_list)

            return [country.capitalize() for country in list_countries]

        elif intext in continent_list:
            temp_data = self._data_cleaning(
                file_location="../data/product_group_CPI/"+intext.lower()+
                "_products_CPI/CPI_Education.csv")

            return temp_data.index.to_list()

        else:
            if intext.endswith("*"):
                list_countries_specific = []
                for country in list_countries:
                    if country.startswith(intext[:-1]):
                        list_countries_specific.append(country)
                return [country.capitalize() for country in list_countries_specific]
            else:
                list_countries_specific = []
                for country in list_countries:
                    if intext in country:
                        list_countries_specific.append(country)
                return [country.capitalize() for country in list_countries_specific]


    def by_country(self, product:str, cl:list) -> pd.DataFrame:
        '''
        Returns data with selected countries.

        Parameters
        ----------
        product : str
            product to be filtered.
        country_list : list
            countries to be filtered.

        Returns
        -------
        data_countries : Pandas dataframe
            returns Pandas dataframe with selected product and countries.

        '''
        self.product = product
        self.cl = cl
        cl = [c.capitalize() for c in cl]
        logging.basicConfig(level=logging.INFO)

        # for index, country in enumerate(country_list):
        #     country_list[index] = country_list[index].capitalize()
        logging.info(bcolors.OKGREEN+f"You have chosen the following countries : {cl}"
                     +bcolors.ENDC)

        data = self.by_product(product)
        available_countries = [country for country in cl if country in data.index]
        wrong_countries = [country for country in cl if country not in data.index]

        data_countries = data.loc[available_countries]
        if len(wrong_countries) != 0:
            print(f"These countries are not available or misspelled:\n {wrong_countries}")
        return data_countries


    def list_years(self) -> list:
        '''
        List years available in a data file

        Returns
        -------
        available_time : list
            list with possible time entries.

        '''

        data = self.by_country(self.product, self.cl)
        available_time = data.columns.values

        return available_time


    def by_year(self, product:str, cl:list, start, stop) -> pd.DataFrame:
        '''
        Returns data with selected years.

        Parameters
        ----------
        product : str
            DESCRIPTION.
        country_list : list
            DESCRIPTION.
        start : TYPE
            DESCRIPTION.
        stop : TYPE
            DESCRIPTION.

        Returns
        -------
        data_years : TYPE
            DESCRIPTION.

        '''
        start = start.capitalize()
        stop = stop.capitalize()
        data = self.by_country(product,cl)
        if (start in data.columns.values) and (stop in data.columns.values):
            wanted_columns = data.columns.values[np.where(data.columns.
                                                        values == start)[0][0]:
                                                np.where(data.columns.
                                                        values == stop)[0][0]]
            data_years = data[wanted_columns]
            logging.basicConfig(level=logging.INFO)
            logging.info(bcolors.OKGREEN+f"You have chosen the time data from \
                         {wanted_columns[0]} to {wanted_columns[-1]}"
                        +bcolors.ENDC)

            return data_years
        else:
            print(f"Either '{start}' or '{stop}' is incorrect.")
            print("Available periods are :")
            print(data.columns.values)


    @staticmethod
    def _get_relative_data_directory():
        '''
        A static function, it return relative directory of a data. 

        Returns
        -------
        data_dir : TYPE
            DESCRIPTION.

        '''
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.abspath(os.path.join(current_dir, os.pardir, 'data'))

        return data_dir


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(args):
    """
    The main entry function from the command line interface.

    Parameters
    ----------
    args : TYPE
        Accepts arguments product,country list, period of time from command line.

    Returns
    -------
    None.

    """
    prpr = Preprocessor()
    no_product = (not args.product or args.product is None)
    no_countries = (not args.countries or args.countries is None)
    no_time = not args.time

    if no_product:
        logging.error(bcolors.FAIL+"Missing argument : -p, --products is required."
                      +bcolors.ENDC)
        print(prpr.list_products())
    else:
        if no_countries:
            prpr.by_product(args.product)
            logging.warning(bcolors.WARNING+"Missing argument : -c, --countries\
                            can be specified."
                         +bcolors.ENDC)
            print(prpr.list_countries())
        else:
            if no_time:
                prpr.by_country(args.product,args.countries)
                logging.warning(bcolors.WARNING+"Missing argument : -t, --time \
                                can be specified. Correct format: "+
                      'start:Month_year  end:Month_year e.g Jan_2010 Dec_2012'+bcolors.ENDC)
                print(prpr.list_years())
            else:
                start,stop = args.time
                data = prpr.by_year(args.product,args.countries,start,stop)
                print(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--product', type=str, help='Product name')
    parser.add_argument('-c', '--countries', nargs='+', help='List of countries')
    parser.add_argument('-t', '--time', type=str, nargs=2, help='Start, Stop')

    args = parser.parse_args()
    main(args)
