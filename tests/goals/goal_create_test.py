from rest_framework import status

import pytest


@pytest.mark.django_db
def test_success(auth_client, goal_1):

    data = {
        "title": goal_1.title,
    }

    response = auth_client.post(
        "/goals/goal/create",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == goal_1.title


@pytest.mark.django_db
def test_unauthorized(client, goal_1):

    data = {
        "title": goal_1.title,
    }

    response = client.post(
        "/goals/goal/create",
        data=data,
        content_type='application/json'
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
