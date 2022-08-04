from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter
from goals.models import Goal, Status
from goals.permissions import GoalPermissions
from goals.serializers import GoalCreateSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ["priority", "due_date"]
    ordering = ["priority", "due_date"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Status.ARCHIVED
        instance.save()
        return instance
