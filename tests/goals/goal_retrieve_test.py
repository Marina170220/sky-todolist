import pytest
from rest_framework import status


from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal_1):
    response = auth_client.get(f"/goals/goal/{goal_1.id}",
                          content_type='application/json'
                          )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == GoalSerializer(goal_1).data
