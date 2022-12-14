from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from goals.models import Comment
from goals.permissions import CommentPermissions
from goals.serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [CommentPermissions]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [CommentPermissions]
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["goal"]
    ordering = ["-id"]

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user_id=self.request.user.pk)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        return Comment.objects.filter(goal__category__board__participants__user_id=self.request.user.pk)
