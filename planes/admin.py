from django.contrib import admin

from planes.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'username',
        'is_staff',
        'is_active',
        'is_admin',
    ]
    search_fields = ('username', 'email')
