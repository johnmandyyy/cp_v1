# Generated by Django 3.2.18 on 2023-05-31 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20230531_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_dataset', models.IntegerField(default=0)),
                ('validation_set', models.IntegerField(default=0)),
                ('training_dataset', models.IntegerField(default=0)),
                ('testing_dataset', models.IntegerField(default=0)),
                ('validation_acc', models.FloatField(default=0)),
                ('testing_acc', models.FloatField(default=0)),
            ],
        ),
    ]
