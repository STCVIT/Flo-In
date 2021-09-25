from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .Forms import UserAdminCreationForm, UserAdminChangeForm
from .models import MyUser, UserData, FaceData
from django.contrib.auth.models import Group
from django.contrib import admin


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("email", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(UserData)
admin.site.register(FaceData)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
