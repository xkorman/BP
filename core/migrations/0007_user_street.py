# Generated by Django 3.1.6 on 2021-02-23 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210223_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='street',
            field=models.TextField(default=23),
            preserve_default=False,
        ),
    ]
