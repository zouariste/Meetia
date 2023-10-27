from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import (
    ImageField,
    ModelForm,
    forms,
    CharField,
    IntegerField,
    HiddenInput,
)

from .models import User, Employe


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("email",)


class EmployeEditForm(UserChangeForm):
    avatar = ImageField()
    password = CharField(widget=HiddenInput())

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "sexe",
            "poste",
        )
