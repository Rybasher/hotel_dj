# Generated by Django 3.2.5 on 2021-07-28 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_roomimage_text'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Museum',
            new_name='SightseeingMuseum',
        ),
        migrations.RenameModel(
            old_name='NightGuide',
            new_name='SightseeingNightGuide',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='hotel',
            options={'verbose_name': 'hotel', 'verbose_name_plural': 'hotels'},
        ),
        migrations.AlterModelOptions(
            name='sightseeingadditem',
            options={'verbose_name': 'sightseeing_add_item', 'verbose_name_plural': 'sightseeing_add_items'},
        ),
        migrations.AlterModelOptions(
            name='sightseeingguide',
            options={'verbose_name': 'sightseeing_guide', 'verbose_name_plural': 'sightseeing_guides'},
        ),
        migrations.AlterModelOptions(
            name='sightseeingmuseum',
            options={'verbose_name': 'sightseeing_museum', 'verbose_name_plural': 'sightseeing_museums'},
        ),
        migrations.AlterModelOptions(
            name='sightseeingnightguide',
            options={'verbose_name': 'sightseeing_museum', 'verbose_name_plural': 'sightseeing_museums'},
        ),
        migrations.AlterModelOptions(
            name='socialmedia',
            options={'verbose_name': 'social_media', 'verbose_name_plural': 'social_medias'},
        ),
    ]
