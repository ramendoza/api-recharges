from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "read_key", "write_key")
    search_fields = ("user__username", "user__email", "read_key", "write_key")
