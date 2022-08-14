from pytest_factoryboy import register

from tests.factories import UserFactory, BoardFactory, BoardParticipantFactory, CategoryFactory, GoalFactory

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(CategoryFactory)
register(GoalFactory)
