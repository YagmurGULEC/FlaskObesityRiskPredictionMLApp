#!/usr/bin/env bash

# Build image
docker build -t myflaskapp .

# List docker images
docker image ls

# Run flask app
docker run -p 5000:5000 myflaskapp
