# Generated by Django 3.2.11 on 2022-01-19 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_article_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
    ]