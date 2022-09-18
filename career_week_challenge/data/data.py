import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.cloud import storage, bigquery

def Get_data():
    """retrieves data from csv and returns DataFrame"""

    #loading data
    filepath = os.path.join('..','raw_data', 'dataset.csv')
    data = pd.read_csv(filepath, sep=';')

    # test and train data
    test_data= data[data['default'].isnull()]
    train_data =data.drop(index=test_data.index)
    X_train = train_data.drop(columns=['default', 'uuid'], axis=1)
    y_train = train_data['default']

    return X_train, y_train, test_data
