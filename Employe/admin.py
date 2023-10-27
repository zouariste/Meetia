from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import User


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
        "avatar",
        "phone",
        "poste",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)


class EmployeAdmin(admin.ModelAdmin):
    fields = ("user",)
    model = Employe
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "sexe",
        "avatar",
        "poste",
        "is_active",
    )


admin.site.register(User, UserAdmin)
admin.site.register(Rapporteur, EmployeAdmin)
admin.site.register(Collaborateur, EmployeAdmin)
admin.site.register(Dirigeant, EmployeAdmin)
