#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This plotter class provides plotting functions using previous analysis and cleaning.
It saves plots as images in results folder within repository


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
import sys
import argparse
import yaml
import matplotlib as mpl
from analysis import Analyser
from matplotlib import pyplot as plt
import pandas as pd


class Plotter:
    """
    Plotter class plot a chart based on the result of analysis.
    """

    def __init__(self, data: pd.DataFrame, title):
        self.data = data
        self.title = title


    def plot_bar(self):
        """
        Plot a bar chart representing the inflation rates across different countries over months.
    
        This function takes the data stored in the object and plots a bar chart where each country's
        inflation rate is shown for every month. The months are displayed on the x-axis, and the
        inflation rates are displayed on the y-axis.
    
        Returns:
            matplotlib.figure.Figure: The generated bar chart figure.
    
        Example usage:
            Suppose you have a data object named 'data_obj' with the appropriate data and title set.
            You can use the plot_bar() method as follows:
    
            fig = data_obj.plot_bar()
            plt.show()
        """
        data_t = self.data.transpose()

        x_ticks = data_t.index


        plt.figure(figsize=(12, 6))
        bar_width = 0.6

        bottom = [0] * len(data_t)

        for country in data_t.columns:
            plt.bar(x_ticks, data_t[country], bar_width, label=country, bottom=bottom)
            bottom = [bottom[i] + data_t[country][i] for i in range(len(data_t))]

        plt.xlabel("Months")
        plt.ylabel("Inflation Rate")
        plt.title(self.title)
        plt.xticks(rotation=90)
        plt.legend(loc="upper right")
        plt.grid(True)

        plt.tight_layout()

        return plt.gcf()


    def plot_line(self):
        """
        Plot a line chart representing the inflation rates across different 
        countries over months.
        
        This function takes the data stored in the object and plots a line chart
        where each country's inflation rate is shown as a line plot for every month.
        The months are displayed on the x-axis, and the inflation rates are displayed
        on the y-axis.
        
        Returns:
            matplotlib.figure.Figure: The generated line chart figure.
        
        Example usage:
            Suppose you have a data object named 'data_obj' with the appropriate
            data and title set. You can use the plot_line() method as follows:
        
            fig = data_obj.plot_line()
            plt.show()
        """
        data_t = self.data.transpose()

        x_ticks = data_t.columns

        plt.figure(figsize=(12, 6))
        for country in data_t.columns:
            plt.plot(data_t.index, data_t[country], label=country)

        plt.xlabel("Months")
        plt.ylabel("Inflation Rate")
        plt.title(self.title)
        plt.xticks(rotation=90)
        plt.legend(loc="upper right")
        plt.grid(True)

        plt.tight_layout()

        return plt.gcf()


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

    analyser = Analyser()

    #working directories
    current_dir = os.path.dirname(__file__)
    results_dir = os.path.abspath(os.path.join(current_dir, '..', 'results'))
    bin_dir = os.path.abspath(os.path.dirname(__file__))

    #set plot config if given
    if args.plotparams:
        try:
            assert args.plotparams in ('bigplot', 'smallplot')
            if args.plotparams == 'bigplot':
                file = os.path.abspath(os.path.join(bin_dir, 'bigplot.yml'))
            if args.plotparams == 'smallplot':
                file = os.path.abspath(os.path.join(bin_dir, 'smallplot.yml'))
            with open(file, 'r') as reader:
                plot_params = yaml.load(reader, Loader=yaml.BaseLoader)

            for param, value in plot_params.items():
                mpl.rcParams[param] = value
        except AssertionError:
            sys.exit('options for plotparams are only bigplot or smallplot')

    #type of analysis
    total = args.analysis == 'total'
    product = args.analysis == 'product'

    #type of plot
    default = args.graphic == 'all'
    bar = args.graphic == 'bar'
    line = args.graphic == 'line'
    
    start,stop = args.time
    start = start.capitalize()
    stop = stop.capitalize()

    if total:
        try:
            assert len(args.countries) == 1
            country = args.countries[0]
            inflation_data = analyser.all_products_inflation(country, start, stop)
            title = f'Inflation Rate in {country} for all products'
            output = f'inflation_rate_all_products_{country}'
        except AssertionError:
            sys.exit('only one country is allowed if the total analysis is chosen')
        except IndexError:
            sys.exit('the time is not correct. It must be, for example: Jan_2021 Dec_2022')
        except AttributeError:
            sys.exit('Time not written correctly')

    if product:
        try:
            assert isinstance(args.product, str)
            args.product = args.product.title()
            analyser.by_product(args.product)
            analyser.by_country(args.product,args.countries)
            data = analyser.set_datafile(args.product,args.countries,start,stop)
            inflation_data = analyser.inflation_calculator(data)
            title = f'Inflation Rate across Countries for {args.product}'
            output = f'inflation_rate_{args.product}'
        except AssertionError:
            sys.exit('product must be given if product analysisis is chosen')
        except KeyError as e:
            sys.exit(f'a country given is not in the list {e}')
        except IndexError:
            sys.exit('the time is not correct. It must be, for example, like: Jan_2021 Dec_2022')
        except AttributeError:
            sys.exit('Time not written correctly')

    plotter = Plotter(inflation_data, title)

    #output names
    bar_output = os.path.abspath(os.path.join(results_dir, f'{output}_bar.png'))
    line_output = os.path.abspath(os.path.join(results_dir, f'{output}_line.png'))

    if default:
        bar_plot = plotter.plot_bar()
        bar_plot.savefig(bar_output, dpi=300)
        line_plot = plotter.plot_line()
        line_plot.savefig(line_output, dpi=300)
    elif bar:
        bar_plot = plotter.plot_bar()
        bar_plot.savefig(bar_output, dpi=300)
    elif line:
        line_plot = plotter.plot_line()
        line_plot.savefig(line_output, dpi=300)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-p', '--product', type=str, help='Product name')
    parser.add_argument('-c', '--countries', nargs='+', help='List of countries',
                        required=True)
    parser.add_argument('-t', '--time', type=str, nargs=2, help='Start, Stop',
                        required=True)
    parser.add_argument('-g', '--graphic', type=str, help='type of plot: line or bar',
                        default='all')
    parser.add_argument('-a', '--analysis', type=str, help='type of analysis: \
                        total or product',
                        required=True)
    parser.add_argument('--plotparams', type=str, help='Matplotlib parameters \
                        (YAML file) options: big',
                        default=None)

    args = parser.parse_args()

    main(args)
