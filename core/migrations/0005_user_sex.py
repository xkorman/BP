# Generated by Django 3.1.6 on 2021-02-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('F', 'Zena'), ('M', 'Muz'), ('O', 'Ine')], default=0, max_length=1),
            preserve_default=False,
        ),
    ]
