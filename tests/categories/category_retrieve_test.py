import pytest
from rest_framework import status


from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_retrieve_category(auth_client, category_1):
    response = auth_client.get(f"/goals/goal_category/{category_1.id}",
                          content_type='application/json'
                          )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == BoardSerializer(category_1).data
