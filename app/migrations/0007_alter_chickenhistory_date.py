# Generated by Django 3.2.18 on 2023-05-18 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_chickens_verdict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chickenhistory',
            name='date',
            field=models.DateField(default=models.DateField(auto_now=True), null=True),
        ),
    ]
