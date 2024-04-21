import pytest
from flask import g, session
from app.init_app import init_app




@pytest.mark.parametrize(
    ("data"),
    (  #data with missing key values
        {  
            "Height":1.57,
            "Weight":64.0,
            "Age":21.0,
            "family_history_with_overweight":"yes",
            "FAVC":"yes","FCVC":2.0,"NCP":3.0,
            "CAEC":"Sometimes","SMOKE":"no","CH2O":2.0,
            "SCC":"no","FAF":0.0,"TUE":1.0,
            "CALC":"Sometimes",
            "MTRANS":"Public_Transportation"},
            #data out of range
            {
            "Gender": "Male",
            "Age": 21.0,
            "Height": 157,
            "Weight": 64.0,
            "family_history_with_overweight": "yes",
            "FAVC": "yes",
            "FCVC": 2.0,
            "NCP": 3.0,
            "CAEC": "Sometimes",
            "SMOKE": "no",
            "CH2O": 2.0,
            "SCC": "no",
            "FAF": 0.0,
            "TUE": 1.0,
            "CALC": "Sometimes",
            "MTRANS": "Public_Transportation"
    },
            
    )
)
def test_validate_wrong_input(client, data):
    
    response=client.post("/predict",headers={"Content-Type": "application/json"},json=data)
    assert response.json['data']['error']=="Data not in the right format"
    


@pytest.mark.parametrize(
    ("data"),
    (
        #test with the right input
        {
            "Gender": "Male",
            "Age": 21.0,
            "Height": 1.57,
            "Weight": 64.0,
            "family_history_with_overweight": "yes",
            "FAVC": "yes",
            "FCVC": 2.0,
            "NCP": 3.0,
            "CAEC": "Sometimes",
            "SMOKE": "no",
            "CH2O": 2.0,
            "SCC": "no",
            "FAF": 0.0,
            "TUE": 1.0,
            "CALC": "Sometimes",
            "MTRANS": "Public_Transportation"
    },
    #test with the right input but not in the same order
    {   
             "Age": 21.0,
            "Gender": "Male",
           "Height": 1.57,
            "Weight": 64.0,
            "family_history_with_overweight": "yes",
            "FAVC": "yes",
            "FCVC": 2.0,
            "NCP": 3.0,
            "SMOKE": "no",
            "CH2O": 2.0,
            "SCC": "no",
            "FAF": 0.0,
            "TUE": 1.0,
            "CALC": "Sometimes",
            "MTRANS": "Public_Transportation",
            "CAEC": "Sometimes",
    },
    {   
           
            "Gender": "Male",
            "Height": 1.57,
            "Weight": 64.0,
            "family_history_with_overweight": "yes",
            "FAVC": "yes",
            "FCVC": 2.0,
            "NCP": 3.0,
            "SMOKE": "no",
            "SCC": "no",
            "FAF": 0.0,
            "TUE": 1.0,
            "CALC": "Sometimes",
            "MTRANS": "Public_Transportation",
            "CAEC": "Sometimes",
            "CH2O": 2.0,
            "Age": 21.0,
    },
    {   
           
            "Gender": "Female",
            "Height": 1.57,
            "Weight": 64.0,
            "family_history_with_overweight": "yes",
            "FAVC": "yes",
            "FCVC": 2.0,
            "NCP": 3.0,
            "SMOKE": "no",
            "SCC": "no",
            "FAF": 0.0,
            "TUE": 1.0,
            "CALC": "Sometimes",
            "MTRANS": "Public_Transportation",
            "CAEC": "Sometimes",
            "CH2O": 2.0,
            "Age": 21.0,
    },
    )
)
def test_validate_right_input(client, data):
    
    response=client.post("/predict",headers={"Content-Type": "application/json"},json=data)
    print (response.json['data']['prediction'])
    assert response.status_code ==200



