from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User, Questions, Department


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username',)
    ordering = ('username',)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_active',)}),
        ('Permissions', {'fields': ('is_staff',)}),
        ('User info', {'fields': ('first_name', 'last_name', 'email')})
    )
    # fieldsets = UserAdmin.fieldsets + (
    #     ('Roles', {'fields': ('is_editor',)}),
    # )


class QuestionAdmin(admin.ModelAdmin):
    fields = ['question', 'answer']


admin.site.register(User, MyUserAdmin)
admin.site.register(Questions, QuestionAdmin)
