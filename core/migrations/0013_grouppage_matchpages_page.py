# Generated by Django 3.1.6 on 2021-03-03 08:56

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210302_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='Nova skupina stranok', null=None)),
                ('info', models.TextField(null=None)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='Nova stranka')),
                ('content', django_quill.fields.QuillField()),
            ],
        ),
        migrations.CreateModel(
            name='MatchPages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='core.grouppage')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page', to='core.page')),
            ],
        ),
    ]