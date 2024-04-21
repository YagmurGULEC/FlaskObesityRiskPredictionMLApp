import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import argparse
import os
import sys
import json


def create_categorical_mappings(mapping_filename,predict_column='NObeyesdad'):
    with open(mapping_filename) as f:
        mappings=json.load(f)
    classes_decode={v:k for k,v in mappings[predict_column].items()}
    print (classes_decode)
    return classes_decode

def prepare_data(args):
    
    train_data=pd.read_csv(os.path.join(args.dataroot,'train.csv'))
    print (train_data.head())
    print (len(train_data))
    
    test_data=pd.read_csv(os.path.join(args.dataroot,'test.csv'))
    print (len(test_data))
    train_data.drop('id',axis=1,inplace=True)
    print (train_data.columns)
    print (len(train_data.columns))
    
    #save columns in the same order
    mappings=dict((column, None) for column in train_data.columns)
    classes=train_data['NObeyesdad'].unique()
    
    assert (train_data.isnull().sum().sum()==0) 
    assert (test_data.isnull().sum().sum()==0) 
    df_numeric=train_data.select_dtypes(exclude=['object']).columns
    #categorical columns
    categorical=train_data.select_dtypes(include=['object']).columns
    #change catergorical to numerical   
    for i in df_numeric:
        intervals={'interval':[train_data[i].min(),train_data[i].max()]}
        mappings[i]=intervals
    for i in categorical:
        vals=[i for i in range(len(train_data[i].unique()))]
        mappings[i]=dict(zip(train_data[i].unique(),vals))
    for i in mappings:
        if mappings[i] is not None:
            train_data[i]=train_data[i].map(mappings[i])
            if i!='NObeyesdad':
                test_data[i]=test_data[i].map(mappings[i])

    X=train_data.drop('NObeyesdad', axis=1)
    y=train_data['NObeyesdad']
    
    X_train, X_val, y_train, y_val = train_test_split(X,y,test_size=args.validation_split,random_state=42)
    X_test=test_data.drop('id', axis=1).to_numpy()
    
    scaler=StandardScaler()
    X_train=scaler.fit_transform(X_train)
    X_val=scaler.transform(X_val)
    X_test=scaler.transform(X_test)
    print(mappings)
    return X_train, X_val, np.array(y_train), np.array(y_val),X_test,test_data['id'],mappings


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare data for training')
    parser.add_argument('--dataroot', type=str, default='kaggle', help='path to data')
    parser.add_argument('--validation_split', type=float, default=0.2, help='validation split')
    args = parser.parse_args()
    res=prepare_data(args)
    