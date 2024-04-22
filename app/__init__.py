"""Flask app for obesity risk prediction"""

import glob
import os
import json
import argparse
from flask import Flask,request,jsonify,Response
import torch
import torch.nn.functional as F
from .models import FullyConnected
from . import init_app


DEVICE='cuda' if torch.cuda.is_available() else 'cpu'

def get_prediction(x,filename=glob.glob('./kaggle/*.pth')[0]):
    """Function to get a prediction from the model with the given tensor data"""
    assert x.shape[0]==16
    x.unsqueeze(0)
    model_name=filename
    opt = argparse.Namespace(fcn=[10])
    model=FullyConnected(opt)
    checkpoint=torch.load(model_name,map_location=DEVICE)
    model.load_state_dict(checkpoint['net'])
    model.to(DEVICE)
    model.eval()
    with torch.no_grad():
        x=x.to(DEVICE)
        outputs=model(x)
        probs = F.softmax(outputs, dim=1)
    numerical_class=torch.argmax(probs).item()
    with open('predict_decode.json',encoding="utf-8") as f:
        classes_decode=json.load(f)
    return classes_decode['NObeyesdad'][str(numerical_class)]


def convert_to_tensor(data_dict):
    """Function to convert a dictionary to a tensor"""
    data_list=[]
    for v in data_dict.values():
        data_list.append(v)
    return torch.tensor(data_list).float()

def encode_data(data):
    """Function to encode the data to the numerical format for the model"""
    new_data=data.copy()
    with open('mappings.json',encoding="utf-8") as f:
        mappings=json.load(f)
    for k,v in mappings.items():
        if k!='NObeyesdad':
            #only get categorical data to encode
            if v.get('interval') is None:
                new_data[k]=v[data[k]]
    return new_data

#check and order the data
def check_data(data,mappings_file='mappings.json'):
    """Function to check the data and order it according to the mappings file"""
    with  open(mappings_file,encoding="utf-8") as f:
        mappings=json.load(f)
    ordered_data={}
    for k,v in mappings.items():
        if k!='NObeyesdad':
            if data.get(k) is not None:
                ordered_data[k]=data[k]
                if v.get('interval') is not None:
                    if data[k]<v['interval'][0] or data[k]>v['interval'][1]:
                        print ("Data out of range")
                        return False
                else:
                    if data[k] not in v.keys():
                        print ("Data not in the mappings")
                        return False
            else:
                return False
    data.clear()
    data.update(ordered_data)
    return True

def create_app():
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    init_app.init_app(app)
    @app.route('/')
    def index():
        return 'Obesity risk prediction prediction API'
    @app.route('/predict',methods=['POST'])
    def predict():
        json_payload = request.json
        is_passed=check_data(json_payload)
        if is_passed:
            encoded=encode_data(json_payload)
            x=convert_to_tensor(encoded)
            prediction=get_prediction(x)
            resp={"prediction":prediction,'parameters':json_payload}
            return jsonify(data=resp)
        return jsonify(data={"error":"Data not in the right format"})
    return app
