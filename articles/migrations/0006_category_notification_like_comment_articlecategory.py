# Generated by Django 4.1.2 on 2022-10-16 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0005_alter_article_article_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(default='Нет категории', max_length=128, unique=True)),
                ('image', models.CharField(default='', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('message', models.CharField(default='', max_length=512)),
                ('message_readed', models.BooleanField(default=False)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Создатель', to=settings.AUTH_USER_MODEL)),
                ('recipient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Получатель', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('event_type', models.CharField(choices=[('Нравится', 'Нравится'), ('Не нравится', 'Не нравится')], default='Нравится', max_length=32)),
                ('article_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.article', verbose_name='Статья')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('guid', models.CharField(db_column='guic', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('body', models.TextField(default='ici')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('article_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Статья', to='articles.article')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Автор', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('guid', models.CharField(db_column='guid', default=uuid.uuid4, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('article_guid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='articles.article')),
                ('category_guid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.category')),
            ],
        ),
    ]
