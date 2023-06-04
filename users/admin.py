from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("username", "first_name", "last_name", "email")
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Особенные даты', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ("last_login", "date_joined")
    exclude = ("password",)
    ordering = ('email',)


admin.site.unregister(Group)
