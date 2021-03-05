from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User, Questions, Department, Prisoner, MatchPrisoner, GroupPage, Page, MatchPages, ForumCategory


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


class PrisonerAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'date_of_birth', 'prisoner_num', 'department']


class MatchPrisonerAdmin(admin.ModelAdmin):
    fields = ['prisoner_id', 'user_id']


class PageAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'show']


class GroupAdmin(admin.ModelAdmin):
    fields = ['title', 'info']


class MatchPagesAdmin(admin.ModelAdmin):
    fields = ['group', 'page']


class ForumCategoriesAdmin(admin.ModelAdmin):
    fields = ['title']


admin.site.register(User, MyUserAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Prisoner, PrisonerAdmin)
admin.site.register(MatchPrisoner, MatchPrisonerAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GroupPage, GroupAdmin)
admin.site.register(MatchPages, MatchPagesAdmin)
admin.site.register(ForumCategory, ForumCategoriesAdmin)