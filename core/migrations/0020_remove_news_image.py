# Generated by Django 3.1.6 on 2021-03-09 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_news_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
    ]
