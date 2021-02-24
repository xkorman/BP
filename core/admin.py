from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User, Questions, Department


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username',)
    ordering = ('username',)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_active', )}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('User info', {'fields': ('first_name', 'last_name', 'email', 'sex', 'city', 'street', 'date_of_birth')})
    )
    fieldsets = UserAdmin.fieldsets + (
        ('User info', {'fields': ('sex', 'city', 'street', 'date_of_birth')}),
    )


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'answer']


admin.site.register(User, MyUserAdmin)
admin.site.register(Questions, QuestionAdmin)
