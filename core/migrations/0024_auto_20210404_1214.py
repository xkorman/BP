# Generated by Django 3.1.6 on 2021-04-04 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_prisoner_department'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': ('Ústav',), 'verbose_name_plural': 'Ústavy'},
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('type', models.CharField(choices=[('N', 'Žiadosť o návštevu'), ('T', 'Žiadosť o telefonát'), ('V', 'Žiadosť o videohovor')], default='N', max_length=1)),
                ('state', models.CharField(choices=[('R', 'Rieši sa'), ('S', 'Schválaná'), ('F', 'Zamietnutá'), ('P', 'Poslaná')], default='P', max_length=1)),
                ('prisoner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.prisoner')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Žiadosti',
            },
        ),
    ]
