# Generated by Django 3.2.18 on 2023-05-31 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20230528_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptom',
            name='belongs_to',
            field=models.CharField(default='No Category', max_length=100),
        ),
        migrations.AddField(
            model_name='symptom',
            name='forecasted_disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='forecasted_disease', to='app.disease'),
        ),
        migrations.AddField(
            model_name='symptom',
            name='is_correct',
            field=models.BooleanField(null=True),
        ),
    ]