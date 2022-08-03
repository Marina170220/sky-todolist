from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('password', )
    readonly_fields = ('last_login', 'date_joined')
    list_display = ('username', 'email', 'first_name', 'last_name', 'password', 'is_staff')
    list_display_links = ('username',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    list_editable = ('password', )
