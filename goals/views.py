from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import Category
from goals.serializers import CategoryCreateSerializer , CategorySerializer


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
