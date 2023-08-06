#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 20:07:59 2023

@author: alejandracamelocruz
"""

from setuptools import setup

setup(
      name = 'global_inflation_analyser',
      version = '0.1',
      author = ['Alejandra Camelo Cruz',
      'Bruk Asrat Tsega',
      'Leon Oparin',
      'Kshitij Kar'],
      packages = ['global_inflation_analyser'],
      install_requires = [
      'pyyaml',
      'matplotlib',
      'pandas',
      'openpyxl'])