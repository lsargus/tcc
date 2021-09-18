# Generated by Django 3.2.4 on 2021-08-22 19:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('descricao', models.TextField(max_length=255)),
                ('sequencia', models.IntegerField()),
                ('data', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
