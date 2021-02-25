from flask import json
from api import app

#4. [BONUS] Contract Testing
#comando para executar no docker e visualizar a saida do print (r) para erro ou acerto (xP)
#docker-compose exec SERVICE
#docker-compose exec api pytest -rxP

def test_hello():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'Hello World!'
 
def test_categorize_works():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({"products":[{"concatenated_tags": "Lembrancinha"},{"concatenated_tags": "Carrinho de Bebê"}]}),
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 200
    
def test_categorize_bad_request():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({}),
        content_type='application/json'
    )
    print(response.data)    
    assert response.status_code == 400
    
def test_categorize_bad_request_invalid_key():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({"product":[{"concatenated_tags": "Lembrancinha"},{"concatenated_tags": "Carrinho de Bebê"}]}),
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 400
    
def test_categorize_bad_request_no_itens():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({"products":[]}),
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 400    
    
def test_categorize_bad_request_no_concatenated_tags():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({"products":[{"concatenated_": "Lembrancinha"},{"concatenated_tags": "Carrinho de Bebê"}]}),
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 400
    
def test_categorize_bad_request_numeric():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({"products":[{"concatenated_tags": "1223456789"},{"concatenated_tags": "Carrinho de Bebê"}]}),
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 400    
    
def test_categorize_bad_request_empty():
    response = app.test_client().post(
        '/v1/categorize',
        data=json.dumps({"products":[{"concatenated_tags": ""},{"concatenated_tags": "Carrinho de Bebê"}]}),
        content_type='application/json'
    )
    print(response.data)
    assert response.status_code == 400