from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin

from lunch.forms import LunchAppUserChangeForm, LunchAppUserCreationForm
from lunch.models import LunchAppUser


class LunchAppUserAdmin(UserAdmin):
    add_form = LunchAppUserCreationForm
    form = LunchAppUserChangeForm
    model = LunchAppUser
    list_display = ["username", "user_type"]


admin.site.register(LunchAppUser, LunchAppUserAdmin)
