#!/bin/bash

sudo docker build -t chatbot .
sudo docker tag chatbot:latest localhost:3000/chatbot:latest
sudo docker push localhost:3000/chatbot:latest
sudo docker image prune
