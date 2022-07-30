from django.contrib import admin

from goals.models import Category, Goal, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated", "is_deleted")
    list_display_links = ("title", )
    list_filter = ('user', 'created')
    search_fields = ("title",)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "user", "status", "created", "updated", "priority", "expires")
    list_display_links = ("title", )
    list_filter = ('user', 'expires', 'category', 'status', 'priority')
    search_fields = ("title", "user")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "goal", "created", "updated")
    list_display_links = ("text", )
    list_filter = ('user', 'goal', 'created')
    search_fields = ("text", "user")
