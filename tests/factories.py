import factory.django

from goals.models import Board, Category, Goal, BoardParticipant, Role
from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('name')
    password = factory.Faker('password')
    email = factory.Faker('email')
#

class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker("word")
    is_deleted = False


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = Role.OWNER


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    board = factory.SubFactory(BoardFactory)
    title = factory.Faker("word")
    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
