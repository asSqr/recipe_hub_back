# Generated by Django 3.1.4 on 2021-06-21 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_hub', '0002_auto_20210616_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='mrepository',
            name='genre',
            field=models.CharField(default='', max_length=8192),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mrepository',
            name='thumbnail',
            field=models.ImageField(default='Test Genre', upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mrepository',
            name='title',
            field=models.CharField(default='Test Title', max_length=8192),
            preserve_default=False,
        ),
    ]