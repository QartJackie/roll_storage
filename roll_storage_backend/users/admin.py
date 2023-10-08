from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Представление пользователя User в админке."""

    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
    )


admin.site.register(User, UserAdmin)
