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
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    street = models.TextField(null=False)
    date_of_birth = models.DateField(blank=False)

    class Meta:
        verbose_name_plural = 'Uzivatelia'

    def __str__(self):
        return self.first_name + " " + self.last_name + " | " + str(self.date_of_birth) + " | " + self.username


class Department(models.Model):
    name = models.CharField(blank=False, max_length=255)
    type = models.CharField(max_length=1024, blank=True)
    lat = models.CharField(max_length=18, blank=True)
    long = models.CharField(max_length=18, blank=True)
    address = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    email = models.TextField(blank=True)
    web = models.TextField(blank=True)
    iban = models.CharField(max_length=24, blank=True)
    acc_name = models.TextField(blank=True)
    acc_adr = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ústav',
        verbose_name_plural = 'Ústavy'


class Questions(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        verbose_name = 'Najcastesia otazka'
        verbose_name_plural = 'Najcastesie otazky'

    def __str__(self):
        return self.question


class Prisoner(models.Model):
    first_name = models.TextField(max_length=255, blank=False)
    last_name = models.TextField(max_length=255, blank=False)
    date_of_birth = models.DateField(blank=False)
    prisoner_num = models.TextField(max_length=255, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name='ustav')

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

    def __str__(self):
        return self.user_id.first_name + " " + self.user_id.last_name + " + " + self.prisoner_id.first_name + " " + \
               self.prisoner_id.last_name + " - ID:" + self.prisoner_id.prisoner_num


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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Kategória fóra'
        verbose_name_plural = 'Kategórie fóra'


class ForumPost(models.Model):
    title = models.TextField(max_length=1024, blank=False, null=False)
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='category')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    created_at = models.DateTimeField(auto_now=False)
    edited_at = models.DateTimeField(auto_now=True)
    text = QuillField()

    class Meta:
        verbose_name = 'Otázka vo fóre'
        verbose_name_plural = 'Otázky fo fóre'

    def __str__(self):
        return self.title


class ForumComment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    created_at = models.DateTimeField(auto_now=False)
    edited_at = models.DateTimeField(auto_now=True)
    text = QuillField()

    def __str__(self):
        return self.creator.first_name + " " + self.creator.last_name + " " + self.created_at.strftime("%d-%m-%Y %H:%M")

    class Meta:
        verbose_name = 'Komentár k príspevku vo fóre'
        verbose_name_plural = 'Komentáre vo fóre'


class MatchForumComment(models.Model):
    forum_post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='post')
    forum_comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name='comment')

    class Meta:
        verbose_name = 'Priradenie komentáru k príspevku vo fóre'
        verbose_name_plural = 'Priradenie komentárov k príspevkom'

    def __str__(self):
        return self.forum_post.title + " + " + self.forum_comment.creator.first_name + " " + \
               self.forum_comment.creator.last_name + " " + self.forum_comment.created_at.strftime("%d-%m-%Y %H:%M")


class News(models.Model):
    title = models.TextField(max_length=1024, blank=False, null=False)
    text = models.TextField()
    visible = models.BooleanField(default=True)
    img = models.ImageField(upload_to='img/uploaded/', blank=True)

    class Meta:
        verbose_name = 'Prezentačný slajd'
        verbose_name_plural = 'Prezentačné slajdy'

    def __str__(self):
        return self.title


class Requests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Používateľ')
    prisoner = models.ForeignKey(Prisoner, on_delete=models.CASCADE, verbose_name='Väzeň')
    reason = models.TextField(verbose_name='Odôvodnenie')
    created_at = models.DateTimeField(auto_now=False, verbose_name='Vytvorené')
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Upravené',)
    answer = models.TextField(blank=True, verbose_name='Odpoveď')

    Types = (
        ('N', 'Žiadosť o návštevu',),
        ('T', 'Žiadosť o telefonát',),
        ('V', 'Žiadosť o videohovor',),
    )

    States = (
        ('R', 'Rieši sa',),
        ('S', 'Schválená',),
        ('F', 'Zamietnutá',),
        ('P', 'Poslaná',),
    )

    type = models.CharField(
        max_length=1,
        choices=Types,
        null=False,
        default='N',
        verbose_name='Typ'
    )

    state = models.CharField(
        max_length=1,
        choices=States,
        null=False,
        default='P',
        verbose_name='Status'
    )

    class Meta:
        verbose_name_plural = 'Žiadosti'

    def get_type_name(self):
        if self.type == 'V':
            return "Žiadosť o videohovor"
        elif self.type == 'T':
            return "Žiadosť o telefonát"
        else:
            return "Žiadosť o návštevu"

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " | " + self.prisoner.prisoner_num + " | " + \
               self.get_type_name()

