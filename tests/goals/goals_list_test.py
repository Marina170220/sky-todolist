from rest_framework import status

import pytest

from goals.serializers import GoalSerializer
from tests.factories import GoalFactory


@pytest.mark.django_db
def test_goals_list_success(auth_client):
    goals = GoalFactory.create_batch(3)

    expected_response = {
        "count": 3,
        "next": None,
        "previous": None,
        "results": GoalSerializer(goals, many=True).data
    }

    response = auth_client.get("/goals/goal/list")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response
