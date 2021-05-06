from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User, Questions, Department, Prisoner, MatchPrisoner, GroupPage, Page, MatchPages, \
    ForumCategory, ForumComment, ForumPost, MatchForumComment, News, Requests, Message


class MyUserAdmin(UserAdmin):
    model = User
    search_fields = ('username',)
    ordering = ('username',)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_active',)}),
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


class ForumPostsAdmin(admin.ModelAdmin):
    fields = ['title', 'text']


class ForumCommentsAdmin(admin.ModelAdmin):
    fields = ['created_at', 'text']


class MatchForumPostsAdmin(admin.ModelAdmin):
    fields = ['forum_comment', 'forum_post']


class NewsAdmin(admin.ModelAdmin):
    fields = ['title', 'text', ('visible', 'image'), 'img']


class DepartmentAdmin(admin.ModelAdmin):
    fields = ['name', 'phone', 'email', 'address', ('acc_adr', 'acc_name', 'iban'), ('lat', 'long'), 'type', 'web']


class RequestsAdmin(admin.ModelAdmin):
    fields = [('user', 'prisoner'), 'reason', ('type', 'state'), 'answer']
    list_filter = ('type', 'state', 'created_at', 'edited_at', 'prisoner__department', 'user')

    def save_model(self, request, obj, form, change):
        user = User.objects.get(id=request.POST['user'])
        new_message = Message.objects.create(sender=request.user, receiver=user,
                                             text='Vasa ziadost s ID#' + str(obj.id) + ' bola aktualizovana.')
        new_message.save()
        super(RequestsAdmin, self).save_model(request, obj, form, change)

    def get_prisoner_department(self, obj):
        return obj.prisoner.department

    def get_pd_str(self, obj):
        print(obj.prisoner.department)
        return str(obj.prisoner.department)

    ordering = ('-edited_at',)
    list_display = ('id', 'type', 'user', 'edited_at', 'get_prisoner_department', 'state')
    list_display_links = ('user', 'type')
    get_prisoner_department.short_description = 'Ústav'
    get_prisoner_department.admin_order_field = 'prisoner__department'
    search_fields = ['user__first_name', 'user__last_name', 'prisoner__first_name', 'prisoner__last_name',
                     'prisoner__prisoner_num', 'prisoner__department__name']



admin.site.register(User, MyUserAdmin)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Prisoner, PrisonerAdmin)
admin.site.register(MatchPrisoner, MatchPrisonerAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(GroupPage, GroupAdmin)
admin.site.register(MatchPages, MatchPagesAdmin)
admin.site.register(ForumCategory, ForumCategoriesAdmin)
admin.site.register(ForumComment, ForumCommentsAdmin)
admin.site.register(ForumPost, ForumPostsAdmin)
admin.site.register(MatchForumComment, MatchForumPostsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Requests, RequestsAdmin)
