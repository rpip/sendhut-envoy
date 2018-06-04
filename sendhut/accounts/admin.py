# -*- coding: utf-8 -*-
from django.contrib import admin

from sendhut.db import BaseModelAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    exclude = ('password', 'metadata')
    list_display = (
        'id',
        'is_superuser',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'created',
        'phone',
        'last_login',
        'identity_verified',
    )
    list_filter = (
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
        'created',
        'last_login',
        'identity_verified',
    )

    change_form_template = 'loginas/change_form.html'
