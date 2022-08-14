from rest_framework import status

import pytest

from goals.serializers import CategorySerializer
from tests.factories import CategoryFactory


@pytest.mark.django_db
def test_goals_list_success(auth_client):
    cats = CategoryFactory.create_batch(2)

    expected_response = {
        "count": 2,
        "next": None,
        "previous": None,
        "results": CategorySerializer(cats, many=True).data
    }

    response = auth_client.get("/goals/goal_category/list")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response
