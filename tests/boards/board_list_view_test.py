from rest_framework import status

import pytest

from goals.serializers import BoardSerializer
from tests.factories import BoardFactory


@pytest.mark.django_db
def test_goals_list_success(auth_client):
    boards = BoardFactory.create_batch(3)

    expected_response = {
        "count": 3,
        "next": None,
        "previous": None,
        "results": BoardSerializer(boards, many=True).data
    }

    response = auth_client.get("/goals/board/list")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_response
