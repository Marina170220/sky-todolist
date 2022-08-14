import pytest
from rest_framework import status


from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_retrieve_board(auth_client, board):
    response = auth_client.get(f"/goals/board/{board.id}",
                          content_type='application/json'
                          )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == BoardSerializer(board).data
