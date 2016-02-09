import pandas as pd
import numpy as np
import os
from tqdm import tqdm


def load_data(dataframe):
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

def read_from_csv_file(name, path='data/csv/'):
    return pd.read_csv(os.path.join(path,name), index_col=0)

def read_from_excel_file(name, path='data/xls/'):
    return pd.read_excel(os.path.join(path,name))

def store_to_csv(df, path='data/csv/', name='jester-data.csv'):
    df.to_csv(os.path.join(path,name))

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