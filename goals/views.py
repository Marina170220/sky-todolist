from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import Category, Goal, Status, Comment
from goals.permissions import CommentPermissions
from goals.serializers import CategoryCreateSerializer, CategorySerializer, GoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer


class CategoryCreateView(CreateAPIView):
    model = Category
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateSerializer


class CategoryListView(ListAPIView):
    model = Category
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["user"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_deleted=False)


class CategoryView(RetrieveUpdateDestroyAPIView):
    model = Category
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = GoalDateFilter
    ordering_fields = ["priority", "expires"]
    ordering = ["priority", "expires"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(category__user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(category__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [IsAuthenticated, CommentPermissions]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["goal"]
    ordering = ["-id"]

    def get_queryset(self):
        return Comment.objects.filter(goal__category__user=self.request.user)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_queryset(self):
        return Comment.objects.filter(goal__category__user=self.request.user)
