# Generated by Django 3.2.5 on 2021-08-12 17:20

import authy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authy', '0002_profile_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=authy.models.user_directory_path, verbose_name='Picture'),
        ),
    ]
