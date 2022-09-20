import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# from google.cloud import storage, bigquery

def Get_data():
    """retrieves data from csv and returns DataFrame"""

    #loading data
    filepath = os.path.join('raw_data', 'dataset.csv')
    data = pd.read_csv(filepath, sep=';')

    # test and train data
    pred_data= data[data['default'].isnull()]
    #save test_data locally
    pred_data_file_path = os.path.join('raw_data', 'pred_data.csv')
    pred_data.to_csv(pred_data_file_path)
    print('########################## PRED DATA SAVED #################')
    #make train_data
    train_data =data.drop(index=pred_data.index)
    X_train = train_data.drop(columns=['default', 'uuid'], axis=1)
    y_train = train_data['default']
    print('######################done################')
    print(X_train.shape, y_train.shape, pred_data.shape)

    return X_train, y_train
