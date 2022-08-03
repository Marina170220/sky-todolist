from rest_framework.permissions import BasePermission, SAFE_METHODS

from goals.models import BoardParticipant, Role


class CommentPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class BoardPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False

        if not request.user.is_authenticated:
            return False

        filters: dict = {"user": request.user, "board": obj}

        if request.method not in SAFE_METHODS:
            filters["role"] = Role.OWNER

        return BoardParticipant.objects.filter(**filters).exists()


