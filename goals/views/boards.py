from django.db import transaction
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import Board, Goal, Status
from goals.permissions import BoardPermissions
from goals.serializers import BoardCreateSerializer, BoardSerializer, BoardListSerializer


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Status.ARCHIVED)
        return instance


class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardListSerializer
    filter_backends = [OrderingFilter]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)
