# Generated by Django 3.2.18 on 2023-05-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_chickens_tag_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickens',
            name='tag_number',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]