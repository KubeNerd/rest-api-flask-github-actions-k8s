import pytest
from application import create_app


class TestApplication:

    @pytest.fixture
    def client(self):
        app = create_app("config.MockConfig")
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Harry",
            "last_name": "Potter",
            "cpf": "641.396.500-21",
            "email": "contato1@harrypotter.com",
            "birth_date": "1996-09-10",
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Harry",
            "last_name": "Potter",
            "cpf": "641.396.500-22",
            "email": "contato2@harrypotter.com",
            "birth_date": "1996-09-10",
        }

    def test_get_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post("/user", json=valid_user)
        assert response.status_code == 201
        response_json = response.get_json()
        assert "message" in response_json
        assert "User ID:" in response_json["message"]

        response = client.post("/user", json=invalid_user)
        assert response.status_code == 400
        response_json = response.get_json()
        assert "error" in response_json
        assert "invalid" in response_json["error"]

    def test_get_user(self, client, valid_user, invalid_user):
        client.post("/user", json=valid_user)
        response = client.get("/user/%s" % valid_user["cpf"])
        assert response.status_code == 200
        response_json = response.get_json()
        assert response_json["first_name"] == "Harry"
        assert response_json["last_name"] == "Potter"
        assert response_json["cpf"] == "641.396.500-21"
        assert response_json["email"] == "contato1@harrypotter.com"
        assert response_json["birth_date"] == "1996-09-10"

        response = client.get("/user/%s" % invalid_user["cpf"])
        assert response.status_code == 404
        response_json = response.get_json()
        assert "error" in response_json
        assert "User does not exist" in response_json["error"]

    def test_delete_user(self, client, valid_user):
        response = client.delete("/user/%s" % valid_user % ["cpf"])
        assert response.status_code == 200
        assert b"deleted" in response.data

        response = client.delete("/user/%s" % valid_user % ["cpf"])
        assert response.data.status_code == 400
        assert b"does not exist in database" in response.data
