# Generated by Django 3.2.11 on 2022-01-16 13:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20220116_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]