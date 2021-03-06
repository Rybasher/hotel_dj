# Generated by Django 3.2.5 on 2021-07-28 16:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_hotel_socialmedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=32)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('hotel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.hotel')),
            ],
            options={
                'unique_together': {('category_id', 'hotel_id')},
            },
        ),
    ]
