import click
from flask import current_app, g
from flask.cli import with_appcontext
import json
import pandas as pd
import os

def init_app(app):
    """Initalize flask CLI"""
    app.cli.add_command(createMAP)
    app.cli.add_command(createJSON)



@click.command("create-map")
@click.argument('dataroot')
@click.argument('prediction_column',default='NObeyesdad')
@with_appcontext
def createMAP(dataroot,prediction_column):
    train_data=pd.read_csv(os.path.join(dataroot,'train.csv'))
    test_data=pd.read_csv(os.path.join(dataroot,'test.csv'))
    train_data.drop('id',axis=1,inplace=True)
    #save columns in the same order
    mappings=dict((column, None) for column in train_data.columns)
    assert (train_data.isnull().sum().sum()==0) 
    assert (test_data.isnull().sum().sum()==0) 
    df_numeric=train_data.select_dtypes(exclude=['object']).columns
    #categorical columns
    categorical=train_data.select_dtypes(include=['object']).columns
    for i in df_numeric:
        intervals={'interval':[train_data[i].min(),train_data[i].max()]}
        mappings[i]=intervals
    for i in categorical:
        vals=[i for i in range(len(train_data[i].unique()))]
        mappings[i]=dict(zip(train_data[i].unique(),vals))
    with open('mappings.json','w') as f:
        json.dump(mappings,f,indent=4)
    click.echo("JSON file created to check the data given to the model")

    
@click.command("create-json")
@click.argument('filename',default='mappings.json')
@click.argument('prediction_column',default='NObeyesdad')
@with_appcontext
def createJSON(filename,prediction_column):
    with open(filename) as f:
        old_maps=json.load(f)
    new_maps={}
    new_maps[prediction_column]={str(v):k for k,v in old_maps[prediction_column].items()}
    with open('predict_decode.json','w') as f:
        json.dump(new_maps,f,indent=4)
    
    click.echo("JSON file created")