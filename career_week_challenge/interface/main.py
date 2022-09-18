import os
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from career_week_challenge.data.data import Get_data
from career_week_challenge.interface.preprocessing import preprocess


def train():
    """train model """

    X_train, y_train , test_data= Get_data()
    X_resampled, y_resampled = preprocess(X_train)
    X_train_proc, X_val_proc, y_train_proc, y_val_proc= train_test_split(X_resampled, y_resampled, test_size=0.3)
    model = LogisticRegression(penalty='l2',solver='newton-cg', max_iter=2000)
    model.fit(X_train_proc, y_train_proc)
    file_name = os.path.join('..','raw_data', 'base_model.sav')
    pickle.dump(model, open(file_name, 'wb'))

def evaluate():
    """evaluate existing model"""
