# Generated by Django 3.1.5 on 2021-03-29 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_proj_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myadm',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]
