from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User
from core.serializers import UserSerializer
from goals.models import Category, Goal, Comment, Board, BoardParticipant, Role


class CategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_board(self, value):
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")

        if not BoardParticipant.objects.filter(
            board=value,
            role__in=[Role.OWNER, Role.WRITER],
            user_id=self.context["request"].user.id
        ).exists():
            raise ValidationError("not owner of category")

        return value


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Category
        read_only_fields = ("id", "created", "updated", "user", "board")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")

        if self.instance.category.board_id != value.board_id:
            raise ValidationError("transfer between projects not allowed")

        return value


class GoalCreateSerializer(GoalSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if not BoardParticipant.objects.filter(
            board=value.board_id,
            role__in=[Role.OWNER, Role.WRITER],
            user_id=self.context["request"].user.id
        ).exists():
            raise ValidationError("not owner of category")

        return value


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_goal(self, value):
        if not BoardParticipant.objects.filter(
            board=value.category.board_id,
            role__in=[Role.OWNER, Role.WRITER],
            user_id=self.context["request"].user.id
        ).exists():
            raise ValidationError("not owner of category")

        return value


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ("id", "created", "updated", "user", "goal")
        fields = "__all__"


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=Role.OWNER
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices= Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = self.context['request'].user
        new_participants = validated_data.pop("participants", [])
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )
            if title := validated_data.get("title"):
                instance.title = title
            instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
