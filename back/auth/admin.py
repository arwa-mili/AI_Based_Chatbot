from django.contrib import admin
from core.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name","is_active","is_staff")
    search_fields = ("email", "name")
    ordering = ("-id",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name","native_language")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff")
        }),
    )
