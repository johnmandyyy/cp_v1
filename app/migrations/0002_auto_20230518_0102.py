# Generated by Django 3.2.18 on 2023-05-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickens',
            name='picture',
            field=models.ImageField(null=True, upload_to='media/chicken_pictures'),
        ),
        migrations.AlterField(
            model_name='chickens',
            name='tag_number',
            field=models.PositiveIntegerField(default=None, unique=True),
        ),
    ]
