import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from imblearn.over_sampling import ADASYN
from career_week_challenge.data.data import Get_data

class ColumnDropper(TransformerMixin, BaseEstimator):
    def __init__(self, columns):
        self.columns = columns
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return X.drop(columns=self.columns, axis=1)
    def get_feature_names_out(self, X, y=None):
        X= self.transform(X)
        return X.columns

def preprocess(X_train:pd.DataFrame, y_train:pd.Series):
    """takes in a dataframe and deos some preprocessing"""

    #get categorical and numerical columns
    categorical_columns = X_train.select_dtypes(include=['object', 'bool']).columns.to_list()
    numerical_columns = X_train.select_dtypes(exclude=['object', 'bool']).columns.to_list()
    #columns to drop because of big % of missing data and also correlation with other features
    columns_to_drop = ['merchant_category', 'worst_status_active_inv']

    #preprocess numerical columns
    preproc_numeric_pipe = make_pipeline(
    SimpleImputer(strategy='median'),
    RobustScaler()
    )
    #pipeline for categorical columns
    preproc_cat_pipe = make_pipeline(
        SimpleImputer(strategy='most_frequent'),
        OneHotEncoder(sparse=False, handle_unknown='ignore')
    )
    #main preprocessing pipeline
    preproc_base_pipeline = make_column_transformer(
        (ColumnDropper(columns_to_drop), columns_to_drop),
        (preproc_numeric_pipe, numerical_columns),
        (preproc_cat_pipe, categorical_columns)
    )
    #preprocess data
    X_train_preprocessed = preproc_base_pipeline.fit_transform(X_train)
    X_train_preprocessed =pd.DataFrame(X_train_preprocessed)
    #Due to uneven % in classes , resample data to add more to minority class
    X_resampled , y_resampled = ADASYN().fit_resample(X_train_preprocessed, y_train)

    return X_resampled, y_resampled
