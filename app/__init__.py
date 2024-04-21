from flask import Flask,request,jsonify,Response
import os
import json
import torch
from .models import FullyConnected
import argparse
import torch.nn.functional as F

DEVICE='cuda' if torch.cuda.is_available() else 'cpu'



def get_prediction(X,filename=
                   'kaggle/fcn_[10]_lr_0.001_batch_size_32_test_batch_size_32_validation_split_0.2_momentum_0.9_arch_fcn_.pth',
                ):
    assert (X.shape[0]==16)
    X.unsqueeze(0)
    model_name=filename
    opt = argparse.Namespace(fcn=[10])
    model=FullyConnected(opt)
    checkpoint=torch.load(model_name,map_location=DEVICE)
    model.load_state_dict(checkpoint['net'])
    model.to(DEVICE)
    model.eval()
    with torch.no_grad():
        X=X.to(DEVICE)
        outputs=model(X)
        probs = F.softmax(outputs, dim=1)
    numerical_class=torch.argmax(probs).item()
    classes_decode=json.load(open('predict_decode.json'))
    return classes_decode['NObeyesdad'][str(numerical_class)]


def convert_to_tensor(data_dict):
    data_list=[]
    for k,v in data_dict.items():
        data_list.append(v)
    return torch.tensor(data_list).float()

def encode_data(data):
    new_data=data.copy()
    mappings=json.load(open('mappings.json'))
    for k,v in mappings.items():
        if k!='NObeyesdad':
            #only get categorical data to encode
            if v.get('interval') is None:
  
                new_data[k]=v[data[k]]
   
    return new_data

#check and order the data
def check_data(data,mappings_file='mappings.json'):
    print (type(data))
    with  open(mappings_file) as f:
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

def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)

    # # Not actually mapping yet
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    if test_config is None:
        # load the instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import init_app
    init_app.init_app(app)    
    
    @app.route('/')
    def index():
        return 'Obesity risk prediction prediction API'
    
    @app.route('/predict',methods=['POST'])
    def predict():
        if request.method == 'POST':
            json_payload = request.json
            isPassed=check_data(json_payload)
            if isPassed:
                encoded=encode_data(json_payload)
                X=convert_to_tensor(encoded)
                prediction=get_prediction(X)
                resp={"prediction":prediction,'parameters':json_payload}
                return jsonify(data=resp)
            else:
                return jsonify(data={"error":"Data not in the right format"})
       

        
        
        
       
    # from . import auth
    # app.register_blueprint(auth.bp)

    return app