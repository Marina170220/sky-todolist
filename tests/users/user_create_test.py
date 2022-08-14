import pytest
from rest_framework import status


@pytest.mark.django_db
def test_sign_up(client, user_1):
    data = {
        "username": user_1.username,
        "password": user_1.password,
        "password_repeat": user_1.password,
    }

    response = client.post(
        "/core/signup",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_user_profile(auth_client, user):

    expected_response = {
        "id": user.pk,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }

    response = auth_client.get(
        "/core/profile",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_unauthorized_profile(client, user_1):

    response = client.get(
        "/core/profile",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_not_found(client):
    response = client.post(
        "/cores/signup",
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
