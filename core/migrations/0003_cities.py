# Generated by Django 3.1.6 on 2021-02-22 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_department_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('municipalityCode', models.TextField()),
                ('municipalityName', models.TextField()),
                ('countyIdentifier', models.IntegerField()),
                ('status', models.TextField()),
            ],
        ),
    ]
