#!/usr/bin/env bash

PORT=5000
echo "Port: $PORT"

# POST method predict
curl -d '{
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
    }'\
     -H "Content-Type: application/json" \
     -X POST http://localhost:$PORT/predict