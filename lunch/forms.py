# Create your forms here.
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from lunch.models import LunchAppUser


class LunchAppUserCreationForm(UserCreationForm):
    user_type = forms.CharField(
        widget=forms.Select(choices=[('employee', 'Employee'), ('restaurant_owner', 'Restaurant Owner')]))

    class Meta:
        model = LunchAppUser
        fields = ("username", "user_type")


class LunchAppUserChangeForm(UserChangeForm):
    user_type = forms.CharField(
        widget=forms.Select(choices=[('employee', 'Employee'), ('restaurant_owner', 'Restaurant Owner')]))

    class Meta:
        model = LunchAppUser
        fields = ("username", "user_type")
