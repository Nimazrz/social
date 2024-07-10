from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', ]
    fieldsets = UserAdmin.fieldsets + (
        ('Aditional Infarmation', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )
