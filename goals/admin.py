from django.contrib import admin

from goals.models import Category, Goal, Comment, Board


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "is_deleted")
    list_display_links = ("title", )
    readonly_fields = ("created", "updated")
    list_filter = ("user", "created", "is_deleted")
    search_fields = ("title",)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "user", "status", "created", "updated", "priority", "due_date")
    list_display_links = ("title", )
    list_filter = ("user", "due_date", "category", "status", "priority")
    search_fields = ("title", "user")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "goal", "created", "updated")
    list_display_links = ("text", )
    list_filter = ("user", "goal", "created")
    search_fields = ("text", "user")


# @admin.register(Board)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("text", "is_deleted", "created", "updated")
#     list_display_links = ("text", )
#     list_filter = ("created", )
#     search_fields = ("text", )
