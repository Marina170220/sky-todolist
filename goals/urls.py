from django.urls import path

from goals.views.category import CategoryCreateView, CategoryListView, CategoryView
from goals.views.comments import CommentCreateView, CommentListView, CommentView
from goals.views.goals import GoalCreateView, GoalListView, GoalView

urlpatterns = [
    path("goal_category/create", CategoryCreateView.as_view()),
    path("goal_category/list", CategoryListView.as_view()),
    path("goal_category/<int:pk>", CategoryView.as_view()),
    path("goal/create", GoalCreateView.as_view()),
    path("goal/list", GoalListView.as_view()),
    path("goal/<int:pk>", GoalView.as_view()),
    path("goal_comment/create", CommentCreateView.as_view()),
    path("goal_comment/list", CommentListView.as_view()),
    path("goal_comment/<int:pk>", CommentView.as_view()),
]