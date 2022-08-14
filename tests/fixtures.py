import datetime

import pytest

from core.models import User
from goals.models import Board, BoardParticipant, Category, Goal, Comment


@pytest.fixture
@pytest.mark.django_db
def auth_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
@pytest.mark.django_db
def user_1():
    return User(username="test_name_1",
                password="test_password_1",
                email="test_1@test.ru")


@pytest.fixture
@pytest.mark.django_db
def user_2():
    return User(username="test_name_2",
                password="test_password_2",
                email="test_2@test.ru")




# @pytest.fixture
# # @pytest.mark.django_db
# def user_2(django_user_model):
#     return django_user_model.objects.create_user(username="test_user_2", password="test_password_2")
#

# @pytest.fixture
# # @pytest.mark.django_db
# def user_login(client, user_1):
#     client.login(username=user_1.username, password=user_1.password)
#     return user_1
#

@pytest.fixture
@pytest.mark.django_db
def goal_1():
    return Goal(id=1, title="goal_1_title")

@pytest.fixture
@pytest.mark.django_db
def goal_2(category_1, user_2):
    return Goal(title="goal_2_title", category=category_1, user=user_2)


@pytest.fixture
# @pytest.mark.django_db
def board():
    return Board(title="test_board_title")


@pytest.fixture
# @pytest.mark.django_db
def category_1(user_1, board):
    return Category(title="test_category_1", user=user_1, board=board)


@pytest.fixture
# @pytest.mark.django_db
def create_category_2(user_1, board):
    return Category.objects.create(title="test_category_2", user=user_1, board=board)


@pytest.fixture
# @pytest.mark.django_db
def create_goal_1():
    return Goal.objects.create(title="test_goal_1", category=create_category_1, due_date="2022-08-14"
                               )


@pytest.fixture
# @pytest.mark.django_db
def create_goal_2():
    return Goal.objects.create(title="test_goal_2", category=create_category_2, due_date="2022-10-10"
                               )

# def make_comments(goal, user):
#     comment = Comment.objects.create(text=COMMENT_TEXT, goal=goal, user=user)
#     comment_2 = Comment.objects.create(text=COMMENT_TEXT_2, goal=goal, user=user)
#     return comment, comment_2


# @pytest.fixture()
# @pytest.mark.django_db
# def user_token(client, django_user_model):
#     username = 'user_test'
#     password = 'password_test'
#
#     django_user_model.objects.create_user(
#         username=username,
#         password=password,
#     )
#
#     response = client.post(
#         "/core/signup",
#         {"username": username,
#          "password": password},
#         format='json'
#     )
#
#     return response.data["access"]
