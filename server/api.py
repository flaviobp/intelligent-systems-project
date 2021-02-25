import os
import numpy as np
import pandas as pd
import sklearn
import pickle
import sys
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
    

#1. Model Loading
model = pickle.load(open(os.getenv("MODEL_PATH"),'rb'))
target_names = ['Decoração','Papel e Cia','Outros','Bebê','Lembrancinhas','Bijuterias e Jóias']

#3. Input Validation
def input_validation():
    try:
        data = request.get_json(force=True)
    except:
        raise Exception("Falha ao decodificar objeto JSON")
    
    if "products" not in data:
        raise Exception("Não contém a chave 'products'.")

    if not (len(data['products']) > 0):
        raise Exception("Nenhuma produto foi informado.")

    concatenated_tags = np.array([])
    for pair in data['products']:
        if "concatenated_tags" not in pair:
            raise Exception("A chave 'concatenated_tags' não foi informada para um produto.")
            
        if (pair['concatenated_tags'] == None) or (not pair['concatenated_tags'].strip()):
            raise Exception("Valor para 'concatenated_tags' não foi informado para um produto.")
        
        if ((pair['concatenated_tags']).isnumeric()==True):
            raise Exception("Valor inválido para 'concatenated_tags', este campo não é numérico.")
        
        concatenated_tags = np.append(concatenated_tags, pair['concatenated_tags'])

    return concatenated_tags
    
    
#2. Categorization Endpoint
@app.route('/v1/categorize',methods=['POST'])
def predict():

    try:
        concatenated_tags = input_validation()
    except Exception as error:
        return {"error": str(error)}, 400

    # make prediction using model loaded from disk as per the data.
    prediction = model.predict(concatenated_tags)

    prediction_names = [target_names[index] for index in prediction]
    
    return jsonify(dict({"categories":prediction_names}))