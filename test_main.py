import os, pytest, random
from jose       import jwt
from datetime   import datetime, timedelta
from main       import app

from core.database import get_test_db

from fastapi.testclient import TestClient
from models.models import User, MailBoxPosition, Letter, MailBox

client = TestClient(app)

class TestMailboxAPI:
    @pytest.fixture(scope = 'session')
    def db(self):
        yield get_test_db()
    
    @pytest.fixture
    def jwt_token(self):
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

    def test_create_mailbox_success(self, jwt_token):
        headers = {"access" : f"{jwt_token}"}
        data = {
            "mailbox_position_id" : 1,
            "name" : "test"
        }
        
        response = client.post("/mailbox/create", headers = headers, json = data )
        
        assert response.status_code == 201

    def test_create_mailbox_fail(self, jwt_token):
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

    def test_check_mailbox_success(self):
        response = client.get('/mailbox/check')

        assert response.status_code == 200
    
    def test_open_mailbox_success(self, jwt_token):
        headers = {"access" : f"{jwt_token}"}

        response = client.get("/mailbox/open", headers = headers)

        assert response.status_code == 200

    def test_open_mailbox_letter_id_success(self, jwt_token):
        headers = {"access" : f"{jwt_token}"}

        response = client.get("/mailbox/open/1", headers = headers)

        assert response.status_code == 200

    def test_report_letter_success(self, jwt_token):
        headers = {"access" : f"{jwt_token}"}

        response = client.post("/mailbox/report/1", headers = headers)

        assert response.status_code == 200
    
    def test_report_letter_failed(self, jwt_token):
        headers = {"access" : f"{jwt_token}"}

        response = client.post("/mailbox/report/99999", headers = headers)

        assert response.status_code == 404

    def test_generate_mock_letter(self, jwt_token, db):
        headers = {"access" : f"{jwt_token}"}

        response = client.get("/mailbox/gen", headers = headers)
        data = response.json()
        
        assert response.status_code == 200
        assert response.json() == data

        letter_id = data['id']

        before_delete_letter = db.query(Letter).filter(Letter.id == letter_id).first()
        db.delete(before_delete_letter)
        db.commit()

        after_delete_letter = db.query(Letter).filter(Letter.id == letter_id).first()
        assert after_delete_letter is None

        


    # def test_delete_letter(self, jwt_token):
    #     headers = {"access" : f"{jwt_token}"}

    #     mailbox_id = self.test_generate_mock_letter(jwt_token)

    #     response = client.get('/mailbox/delete/{mailbox_id}')
        
    #     assert response.status_code == 200