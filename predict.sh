#!/usr/bin/env bash

PORT=5000
echo "Port: $PORT"

# POST method predict
curl -d '{  
   "Gender":"Male","family_history_with_overweight":"yes","FAVC":"yes","FCVC":3,"NCP":3,"CAEC":"Sometimes","SMOKE":"no","CH2O":2,"SCC":"no","FAF":0,"TUE":1,"CALC":"no"
}'\
     -H "Content-Type: application/json" \
     -X POST http://localhost:$PORT/predict