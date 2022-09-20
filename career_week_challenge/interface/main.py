import os
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from career_week_challenge.data.data import Get_data
from career_week_challenge.interface.preprocessing import preprocess, resample_data


def train():
    """train model """

    X_train, y_train = Get_data()
    X_train_preprocessed = preprocess(X_train)
    X_resampled, y_resampled = resample_data(X_train_preprocessed, y_train)
    X_train_proc, X_val_proc, y_train_proc, y_val_proc= train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=10)
    model = LogisticRegression(penalty='l2',solver='newton-cg', max_iter=5000)
    print('############### MODEL MADE ###############')
    model.fit(X_train_proc, y_train_proc)
    print('############### MODEL FIT  ###############')
    file_name = os.path.join('raw_data', 'base_model.sav')
    pickle.dump(model, open(file_name, 'wb'))
    print('############### MODEL SAVED ###############')

def evaluate():
    """evaluate existing model"""
    ##TODO refactor code so you do not repeat yourself
    X_train, y_train= Get_data()
    X_train_preprocessed = preprocess(X_train)
    X_resampled, y_resampled = resample_data(X_train_preprocessed, y_train)
    X_train_proc, X_val_proc, y_train_proc, y_val_proc= train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=10)

    file_name_model = os.path.join('raw_data', 'base_model.sav')
    model = pickle.load(open(file_name_model, 'rb'))
    if model is None:
        train()
        model = pickle.load(open(file_name_model, 'rb'))

    print('################# LOADED MODEL  ###########')
    #score model on precision
    score = cross_val_score(model,X_val_proc, y_val_proc,scoring='precision' ,cv=5)
    avg_score = np.mean(score)
    print(f'##### AVERAGE PRECISION IS {avg_score}')

    return avg_score

def pred(pred_data= None):
    """run prediction using model and save prdiction as csv file  """
    file_name_model = os.path.join('raw_data', 'base_model.sav')
    model = pickle.load(open(file_name_model, 'rb'))
    print(f'###################### MODEL IS LOADED AND IS A  {model}')
    if model is None:
        print(f'################ TRAINING MODEL ............')
        train()
        print(f'################ MODEL TRAINED ##################')
        model = pickle.load(open(file_name_model, 'rb'))

    if pred_data is None:
        pred_data_file_path = os.path.join('raw_data', 'pred_data.csv') # load data to use for prediction
        pred_data = pd.read_csv(pred_data_file_path)

    #TODO refactor code of line below to not repeat yourself
    X_train, y_train = Get_data()
    pred_data_id = pred_data[['uuid']]
    pred_data_features = pred_data.drop(columns=['uuid', 'default'], axis=1)

    preprocessing_pipeline= preprocess(X_train, name='pred')
    pred_data_preprocessed = preprocessing_pipeline.transform(pred_data_features)
    print('################# PRED-DATA_PREPROCESSED ####################')
    print(f'########################## PRED-DATA_PREPROCESSED_SHAPE IS {pred_data_preprocessed.shape}')

    predictions= model.predict_proba(pred_data_preprocessed)
    print('############### PREDICTIONS MADE ###############')
    ### probality for default ==1 ###
    pred_data_id['default']= predictions[:,1]
    prediction_csv_path = os.path.join('raw_data', 'predicted.csv')
    pred_data_id.to_csv(prediction_csv_path)
    print('############### PREDICTIONS SAVED ###############')

if __name__ == '__main__':
    pred()
