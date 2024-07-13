from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', ]
    fieldsets = UserAdmin.fieldsets + (
        ('Aditional Infarmation', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [ 'author' , 'created']
    ordering = ['created'] #sorting
    search_fields = ['description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['writer', 'content', 'post']