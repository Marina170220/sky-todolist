from django import forms
from django.contrib import admin
from django.db import models
from django.db.models import Count

from goals.models import Category, Goal, Comment, Board, BoardParticipant, Role


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.TextField):
            return forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}))
        return super().formfield_for_dbfield(db_field, request, **kwargs)


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    show_change_link = True

    def _get_form_for_get_fields(self, request, obj=None):
        return self.get_formset(request, obj, fields=("title", "status", "priority", "due_date")).form

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "goals_count", "created", "updated", "is_deleted")
    readonly_fields = ("created", "updated")
    list_filter = ("user", "created", "is_deleted")
    search_fields = ("title", "user")
    inlines = (GoalInline, )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_goals_count=Count('goal', distinct=True))
        return queryset

    def goals_count(self, obj):
        return obj._goals_count

    goals_count.short_description = 'Количество целей'


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "priority", "due_date", "comments_count")
    readonly_fields = ("created", "updated")
    list_filter = ("user", "due_date", "category", "status", "priority")
    search_fields = ("title", "user")
    inlines = (CommentInline, )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_comments_count=Count('goal_comments', distinct=True))
        return queryset

    def comments_count(self, obj):
        return obj._comments_count

    comments_count.short_description = 'Количество комментариев'


class BoardParticipantInline(admin.TabularInline):
    model = BoardParticipant
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()

        # queryset = queryset.exclude(role=Role.OWNER)
        return queryset


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "participants_count", "is_deleted")
    search_fields = ("title", )
    list_filter = ("is_deleted", )
    inlines = (BoardParticipantInline, )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('participants')
        return queryset

    def owner(self, obj):
        return obj.participants.filter(role=Role.OWNER).get().user


    def participants_count(self, obj):
        """
        Количество участников доски, включая владельца

        """
        return obj.participants.count()

    owner.short_description = 'Владелец'
    participants_count.short_description = 'Количество участников'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "goal", "created", "updated")
    list_display_links = ("text", )
    list_filter = ("user", "goal", "created")
    search_fields = ("text", "user")


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "board", "role", "created", "updated")
    search_fields = ("user", "board")
    readonly_fields = ("created", "updated")
    list_filter = ("board", "role")
