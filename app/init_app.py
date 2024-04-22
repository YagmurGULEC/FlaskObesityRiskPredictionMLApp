"""Helper command line functions to create JSON files for the model"""
import os
import json
import click
from flask.cli import with_appcontext
import pandas as pd


def init_app(app):
    """Initalize flask CLI"""
    app.cli.add_command(create_mapping_file)
    app.cli.add_command(create_result_decode)

@click.command("create-map")
@click.argument('dataroot')
@with_appcontext
def create_mapping_file(dataroot):
    """Create a JSON file to map the categorical 
    data to numerical data and check the numerical data in the range"""
    train_data=pd.read_csv(os.path.join(dataroot,'train.csv'))
    test_data=pd.read_csv(os.path.join(dataroot,'test.csv'))
    train_data.drop('id',axis=1,inplace=True)
    #save columns in the same order
    mappings=dict((column, None) for column in train_data.columns)
    assert train_data.isnull().sum().sum()==0
    assert test_data.isnull().sum().sum()==0
    df_numeric=train_data.select_dtypes(exclude=['object']).columns
    #categorical columns
    categorical=train_data.select_dtypes(include=['object']).columns
    for i in df_numeric:
        intervals={'interval':[train_data[i].min(),train_data[i].max()]}
        mappings[i]=intervals
    for i in categorical:
        unique_vals=set(train_data[i])
        mappings[i]=dict((str(v),k) for k,v in enumerate(unique_vals))
    with open('mappings.json','w',encoding="utf-8") as f:
        json.dump(mappings,f,indent=4)
    click.echo("JSON file created to check the data given to the model")

@click.command("create-json")
@click.argument('filename',default='mappings.json')
@click.argument('prediction_column',default='NObeyesdad')
@with_appcontext
def create_result_decode(filename,prediction_column):
    """Create a JSON file to map the numerical data to 
    categorical data to represent the results of the model"""
    with open(filename,encoding="utf-8") as f:
        old_maps=json.load(f)
    new_maps={}
    new_maps[prediction_column]={str(v):k for k,v in old_maps[prediction_column].items()}
    with open('predict_decode.json','w',encoding="utf-8") as f:
        json.dump(new_maps,f,indent=4)
    click.echo("JSON file created")
