# Generated by Django 4.1.2 on 2022-10-08 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_remove_articlehistory_blocked_article_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='moderation',
            field=models.BooleanField(default=True),
        ),
    ]
