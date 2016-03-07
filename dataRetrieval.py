import pandas as pd
import numpy as np
import os, re
from tqdm import tqdm
from fnmatch import fnmatch
from scipy.sparse import dok_matrix


class DataRetriever(object):
    
    def __init__(self, directory_name='data/'):
        self.directory_name = directory_name
    
    def read_from_csv_file(self, name):
        return pd.read_csv(os.path.join(self.directory_name+'csv/', name), index_col=0)

    def read_from_excel_file(self, name):
        return pd.read_excel(os.path.join(self.directory_name+'xls/', name))

    def read_from_directory(self, path_to_jokes = 'data/jokes/'):
        data_list = []
        for elem in tqdm(os.listdir(path_to_jokes)):
            if fnmatch(elem, "*.html"):
                with open(os.path.join(path_to_jokes, elem)) as f:
                    data_list.append(f.read())
                f.close()
        return data_list

    def store_to_csv(self, df, path_to_csv = 'data/csv/', name='jester-data.csv'):
        df.to_csv(os.path.join(path_to_csv,name))

    def build_data(self, dataframe):
        data = []
        y = []
        users = set()
        items = set()
        for user, row in tqdm(dataframe.iterrows()):
            for jokeid, rating in row.iteritems():
                if np.abs(rating - 99) > 1:
                    data.append({ "user_id": user, "movie_id": jokeid})
                    y.append(rating)
                    users.add(user)
                    items.add(jokeid)
        return (data, np.array(y), users, items)    

    def index_lookup(self, val, index_by_val, val_by_index):

        if not (val in index_by_val):
            index = len(index_by_val)
            index_by_val[val] = index
            val_by_index.append(val)
        else:
            index = index_by_val[val]

        return index

    def build_sparse_matrix(self, df, row_name, column_name, value_name):
        """
        Method to build sparse matrix from data frame df.
        Parameters
        ----------
        df : pandas.core.frame.DataFrame
        The pandas data frame to construct the sparse matrix representation from.
        row_name : String
        The name of the column in the data frame to extract the rows from.
        column_name : String
        The name of the column in the data frame to extract the columns from.
        value_name : String
        The name of the column in the data frame to extract the values from.
        Returns A, row_values, col_values
        A = sparse matrix
        row
        """
        num_rows = len(df[row_name].unique())
        num_cols = len(df[column_name].unique())
        A = dok_matrix((num_rows, num_cols), dtype=df[value_name].dtype)

        row_by_index = []
        col_by_index = []

        index_by_row = {}
        index_by_col = {}

        for _, df_row in df.iterrows():
            row_value, col_value, value = df_row[row_name], df_row[column_name], df_row[value_name]

            row_index = self.index_lookup(row_value, index_by_row, row_by_index)
            col_index = self.index_lookup(col_value, index_by_col, col_by_index)            
            A[row_index, col_index] = value


        return A, row_by_index, col_by_index
        
    #def set_dataframe(list_df):
    #    row_start = 0
    #    for ind, table in enumerate(list_df):
    #        to_conca = [columns[ind], table]
    #        print 'Shape of table : {}'.format(table.shape)
    #        table = pd.concat(to_conca)
    #        print 'Shape of table : {}'.format(table.shape)
    #        row_end = row_start + table.shape[0]
    #        labels_ = ['#rating']
    #        lab = ['jokes'+str(i) for i in range(1, 101)]
    #        labels_.extend(lab)
    #        table.set_axis(axis=1, labels=labels_)
    #        users = ['user'+str(i) for i in range(row_start, row_end)]
    #        table.set_axis(axis=0, labels=users)
    #        row_start = row_end + 1
    #    return