# Generated by Django 3.1.6 on 2021-05-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20210511_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Vytvorené'),
        ),
    ]