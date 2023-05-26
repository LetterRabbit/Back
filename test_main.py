import os, pytest, random
from jose       import jwt
from datetime   import datetime, timedelta
from main       import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def jwt_token():
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    expire = datetime.utcnow() + timedelta(minutes=90)
    
    user_info = {
        "id" : 2,
        "username" : '김수훈',
        "exp" : expire
    }

    test_token = jwt.encode(user_info, secret_key, algorithm)
    return test_token

def test_create_mailbox_success(jwt_token):
    headers = {"access" : f"{jwt_token}"}
    data = {
        "mailbox_position_id" : 1,
        "name" : "test"
    }
    
    response = client.post("/mailbox/create", headers = headers, json = data )
    
    assert response.status_code == 201

def test_create_mailbox_fail(jwt_token):
    headers = {"access" : f"{jwt_token}"}
    data_no_mailbox_id = {
        "name" : "test"
    }

    data_no_name = {
        "mailbox_position_id" : 1
    }
    
    data = random.choice([data_no_mailbox_id, data_no_name])

    response = client.post("/mailbox/create", headers = headers, json = data )

    assert response.status_code == 422

def test_check_mailbox_success():
    response = client.get('/mailbox/check')

    assert response.status_code == 200

