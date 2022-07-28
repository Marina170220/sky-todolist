from django.contrib import admin

from goals.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


admin.site.register(Category, CategoryAdmin)
