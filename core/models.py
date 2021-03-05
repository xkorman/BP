from django.contrib.auth.models import AbstractUser
from django.db import models
from django_quill.fields import QuillField

from Test_BP import settings


class Cities(models.Model):
    municipalityCode = models.TextField()
    municipalityName = models.TextField()
    countyIdentifier = models.IntegerField()
    status = models.TextField()

    def __str__(self):
        return self.municipalityName


class User(AbstractUser):
    SEX_CHOICES = (
        ('F', 'Zena',),
        ('M', 'Muz',),
        ('O', 'Ine',),
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        null=False,
        default='M'
    )
    is_editor = models.BooleanField(default=False, null=False)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    street = models.TextField(null=False)
    date_of_birth = models.DateField(blank=False)

    class Meta:
        verbose_name_plural = 'Uzivatelia'

    def __str__(self):
        return self.first_name + " " + self.last_name + " | " + str(self.date_of_birth) + " | " + self.username


class Department(models.Model):
    name = models.CharField(blank=False, max_length=255)
    phone = models.TextField()
    email = models.TextField()

    def __str__(self):
        return self.name


class Questions(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = 'Najcastesia otazka'
        verbose_name_plural = 'Najcastesie otazky'


class Prisoner(models.Model):
    first_name = models.TextField(max_length=255, blank=False)
    last_name = models.TextField(max_length=255, blank=False)
    date_of_birth = models.DateField(blank=False)
    prisoner_num = models.TextField(max_length=255, blank=False)
    department = models.IntegerField(null=False)

    def __str__(self):
        return self.prisoner_num + " | " + self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'Väzen'
        verbose_name_plural = 'Väzni'


class MatchPrisoner(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    prisoner_id = models.ForeignKey(Prisoner, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Priradenie vazna'
        verbose_name_plural = 'Priradenie vaznov'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    date = models.DateTimeField(auto_now=True)
    viewed = models.BooleanField(default=False)
    text = models.TextField(blank=False, null=False)


class Page(models.Model):
    title = models.TextField(null=False, default="Nova stranka")
    content = QuillField()
    show = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Stranka'
        verbose_name_plural = 'Stranky'


class GroupPage(models.Model):
    title = models.TextField(null=None, default="Nova skupina stranok")
    info = models.TextField(null=None)

    class Meta:
        verbose_name = 'Skupina stranok'
        verbose_name_plural = 'Skupiny stranok'

    def __str__(self):
        return self.title


class MatchPages(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page')
    group = models.ForeignKey(GroupPage, on_delete=models.CASCADE, related_name='group')

    class Meta:
        verbose_name = 'Priradenie do skupin'
        verbose_name_plural = 'Priradenie stranok do skupin'

    def __str__(self):
        return self.group.title + ' | ' + self.page.title


class ForumCategory(models.Model):
    title = models.TextField(max_length=255, blank=False)


class ForumPost(models.Model):
    title = models.TextField(max_length=1024, blank=False)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='category')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    created_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(auto_now=True)
    text = QuillField()


class ForumComment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    created_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(auto_now=True)
    text = QuillField()


class MatchForumComment(models.Model):
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='post')
    forum_comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name='comment')