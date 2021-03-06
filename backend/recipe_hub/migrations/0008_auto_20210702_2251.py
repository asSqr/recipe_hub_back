# Generated by Django 3.1.4 on 2021-07-02 22:51

from django.db import migrations, models
import django.db.models.deletion
import recipe_hub.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_hub', '0007_auto_20210627_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='MImage',
            fields=[
                ('myuuidmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='recipe_hub.myuuidmodel')),
                ('id_author', models.CharField(max_length=8192)),
                ('image', models.ImageField(upload_to=recipe_hub.models.path_and_rename)),
            ],
            bases=('recipe_hub.myuuidmodel',),
        ),
        migrations.AddField(
            model_name='mrepository',
            name='is_temp',
            field=models.BooleanField(default=False),
        ),
    ]
