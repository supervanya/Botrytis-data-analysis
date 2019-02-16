import pandas as pd
import numpy as np

# this function will read in given excel file and return a list of pandas for each tab of
# the file (must specify a lits of sheet indexes in sheet_nums parameter)
def read_excel(file_name, sheet_nums = [0], na_values=['NA','Na'], column_names=None):
    list_of_pandas = []
    for n in sheet_nums:
        year_df = pd.read_excel(file_name, sheet_name=n, na_values=na_values, names=column_names)
        list_of_pandas.append(year_df)
    df = join_years(list_of_pandas)
    return df

# this fn will join all the pandas inside of list_of_pandas into one df and return it
def join_years(list_of_pandas):
    return pd.concat(list_of_pandas)


    
# aa_2015 = pd.read_excel('data/plants/msk_aa_15-18.xlsx', sheet_name=4, na_values=['NA','Na'], names=column_names)
# aa_2016 = pd.read_excel('data/plants/msk_aa_15-18.xlsx', sheet_name=5, na_values=['NA','Na'], names=column_names)
# aa_2017 = pd.read_excel('data/plants/msk_aa_15-18.xlsx', sheet_name=6, na_values=['NA','Na'], names=column_names)
# aa_2018 = pd.read_excel('data/plants/msk_aa_15-18.xlsx', sheet_name=7, na_values=['NA','Na'], names=column_names)
