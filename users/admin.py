from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import TokenProxy

from users.models import User

admin.site.unregister(EmailAddress)
admin.site.unregister(TokenProxy)
admin.site.unregister(Site)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "avatar", "_role")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if "_role" in form.changed_data:
            obj.role = obj._role
        obj.save()
