## About The Project

This project is named as Global Inflation Analyzer (GIA). It is a python library, and written to give a comprehensive analysis of inflation rate. The library can be used to perform analysis based on a given dataset with the classification standard of classification of individual consumption by purpose (COICOP 2-5-digit hierarchy). 

With the dataset contained data about consumer price index for group of products and services, the library will analyze the following main questions or features: 

      1. How much has inflation changed during the given range of years? 
      2. In what amount, inflation recorded after or before specific year (e.g. COVID-19 or UKRAIN WAR)? 
      3. Which group of products or services is highly affected after specific year? 
      4. In which year was high inflation recorded?
      5. What is the inflation rate of a specific products or services globally?
      6. What is the inflation rate of a specific products or services group (specific Country)?

## Installation

### Repository

Install Global\_Inflation\_Analyser and go to root folder:

```
git clone https://gitup.uni-potsdam.de/kar/global_inflation_analyser
cd global_inflation_analyser
```

After you downloaded our repository, make sure you have Python installed and all the dependencies needed for the project.

>Make sure you are in the folder containing the software. Check it running pwd in terminal. it should end in global\_inflation\_analyser

If you are using conda, you can download all the dependencies, while being in the root folder, with the following command:

```
conda install -e .
```
Otherwhise, for installing it with pip, run:

```
pip install -e .
```

### Package

If you want to use it as a python package, install it with conda, or pip, using the following commands.

## Usage Guides

After you have moved yourself in the repository where you saved the project. You will notice that you have three classes 
provided to you: preprocessor, analysis and the plotter class. With the Preprocessor class the provided data will be 
cleaned and filtered to your User needs. The Analysis class calculates the Inflation rate of the given data set and 
merge all products inflation rate of a given country for specific period of time. The plotter class provides plots 
with the previous analysed data.
Generally if you want to use the Project we would recommend to use the provided Jupyter Notebook and to run all 
the cells in their given order. While running the cells you will notice you need to choose your data set and the years 
you want. After you executed the plotting part, your results will be saved in the results directory where you can look 
up all the plots. 

The second option that you have is to run the separate python files one after another. It means you would run the 
preprocessor.py. Please be aware you need to be in the directory where the code actually is. So if you are for 
example in global_inflation_analyser:

```
# Moving to the Directory
    cd global_inflation_analyser

# Displaying the help
    python preprocessor.py -h

# Example: Specify product name
    python preprocessor.py -p Education

# Example: Specify product name and list of countries
    python preprocessor.py -p Education -c Germany France Italy

# Example: Specify product name, list of countries, and time period
    python preprocessor.py -p Education -c Germany France Italy -t Jan_2010 Dec_2012
```

After that you would run the analysis.py. 

```
# Displaying the help
    python analysis.py -h
    
# Example:     
    python analysis.py -p Education -c Germany France Italy -t Jan_2023 Dec_2023
```
And in the End the plotter.py.
``` 
# Displaing the help 
    python plotter.py

# Example:     
    python plotter.py -p "productname" -c "country1" "country2" -t "Jan_2021" "Dec_2022" -a "product"

```


After that you should be again able to look up the plots in the results directory. 

## Features

- Comparison Table
- Line Plot Diagramm
- Bar Plot Diagramm
- Boxplot Diagramm
- Dataset can be adjusted 
  - Years adjustable
  - Product adjustable

## Documentation

Please see [Global Inflation Analyzer documentation](#) for more information. 

## Code of conduct

Our code of conduct can be found in the code of [CONDUCT.md](./CONDUCT.md) file in the global_inflation_analyser 
repository.

## Contribution Guidelines

Contributions are always welcome, if you want to find out how to contribute to the Project read the 
[CONTRIBUTING.md](./CONTRIBUTING.md).

## License

Distributed under the **GNU GENERAL PUBLIC LICENSE**. See [LICENSE.txt](./LICENSE.txt) for more information.

## Contact Information

If you have any question regarding this library, please feel free to get in touch with us via the following methods:

+ E-Mail: [leon.oparin@uni-potsdam.de](mailto:leon.oparin@uni-potsdam.de),
          [tsega@uni-potsdam.de](mailto:tsega@uni-potsdam.de),
          [kar@uni-potsdam.de](mailto:kar@uni-potsdam.de),
          [Camelocruz@uni-potsdam.de](mailto:Camelocruz@uni-potsdam.de)

## Acknowledgement

We would like to thank the whole Group and the University of Potsdam for the Opportunity to work 
on such a project and give us the needed knowledge in order to make such a project.
