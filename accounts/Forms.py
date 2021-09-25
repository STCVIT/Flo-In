from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst
from .models import MyUser, UserData, FaceData


class UserAdminCreationForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ("email",)


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ("email", "password", "is_active", "is_admin")


class AuthenticationForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Please enter a correct %(email)s and password. "
        "Note that both fields may be case-sensitive.",
        "inactive": "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields["email"].label is None:
            self.fields["email"].label = capfirst(self.username_field.verbose_name)


class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ["url", "username", "password"]


class FaceDataForm(forms.ModelForm):
    class Meta:
        model = FaceData
        fields = [
            "data",
        ]
