from pydantic import BaseModel
import pytest
import requests


class AccessTokenRequest(BaseModel):
    access_token: str


class User(BaseModel):
    id: int
    first_name: str
    second_name: str


def test_access_token_required():
    request = {
        "access_token": "token123"
    }
    AccessTokenRequest(**request)


def test_users_get_response():
    response = [
        {"id": 345, "first_name": "Alex", "second_name": "Hit"},
        {"id": 678, "first_name": "Oleg", "second_name": "Hit2"}
    ]
    users = [User(**user) for user in response]


def test_access_token():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)



def test_users_get_success():
    response = [
        {"id": 345, "first_name": "Alex", "second_name": "Hit"},
        {"id": 678, "first_name": "Oleg", "second_name": "Hit2"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[0].first_name == "Alex"
    assert users[0].second_name == "Hit"
    assert users[1].id == 678
    assert users[1].first_name == "Oleg"


def test_users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def test_user_format():
    user = {
        "id": "invalid_id_format",
        "first_name": "Alex",
        "second_name": "Hit"
    }
    with pytest.raises(ValueError):
        User(**user)



def test_user_second_name_format():
    user = {
        "id": 345,
        "first_name": "Alex",
        "last_name": "Hit111"
    }
    with pytest.raises(ValueError):
        User(**user)




def test_users_get_one_user():
    response = [{"id": 678, "first_name": "Oleg", "second_name": "Hit2"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 678
    assert users[0].first_name == "Oleg"
    assert users[0].second_name == "Hit2"


def test_users_get_max_users():
    response = [{"id": i, "first_name": "User", "second_name": str(i)} for i in range(1000)
                ]
    users = [User(**user) for user in response]
    assert len(users) == 1000
    assert users[-1].id == 999
    assert users[-1].first_name == "User"
    assert users[-1].second_name == "999"


def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]
