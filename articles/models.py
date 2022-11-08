import uuid

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from users.models import User, UserProfile


# Create your models here.
class Category(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    name = models.CharField(max_length=128, default='Нет категории', unique=True, null=False,
                            verbose_name='Наименование')
    image = models.CharField(max_length=255, null=False, default='', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активность')

    @staticmethod
    def choices():
        return [(blog.guid, blog.name) for blog in Category.objects.filter(is_active=True)]

    def __str__(self):
        return f'{self.name}'

    class Meta:
        indexes = [models.Index(fields=['name'])]
        ordering = ['name']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = 'category'


class Article(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    author_id = models.ForeignKey(User, db_column='author_id', on_delete=models.CASCADE, verbose_name='Автор')
    creation_date = models.DateField(db_column='creation_date', auto_now_add=True, db_index=True,
                                     verbose_name='Дата создания')
    topic = models.CharField(max_length=1024, null=False, verbose_name='Тема')
    article_body = models.TextField(default='ici', null=False, verbose_name='Содержание')
    blocked = models.BooleanField(default=False, verbose_name='Заблокирована')
    moderation = models.BooleanField(default=True, verbose_name='На модерации')
    publication = models.BooleanField(default=False, verbose_name='Видимость статьи')

    def __str__(self):
        return f'Статья {self.topic}, ' \
               f'автор: {self.author_id.email} ' \
               f'от {self.creation_date}'

    class Meta:
        indexes = [models.Index(fields=['blocked']), models.Index(fields=['moderation'])]
        ordering = ['-creation_date']
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        db_table = 'article'


class ArticleCategory(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    category_guid = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, verbose_name='Категория')
    article_guid = models.ForeignKey(Article, on_delete=models.CASCADE, null=False, verbose_name='Статья')

    def __str__(self):
        return f'{self.article_guid.topic} : {self.category_guid.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category_guid', 'article_guid'], name="%(app_label)s_%(class)s_unique")
        ]
        verbose_name = "Категория статьи"
        verbose_name_plural = "Категории статей"
        db_table = 'article_category'


class ArticleHistory(models.Model):
    CREATE = 'Создание'
    EDIT = 'Изменение'
    BLOCK = 'Блокировка'

    ARTICLE_STATUSES = (
        (CREATE, 'Создание'),
        (EDIT, 'Редактирование'),
        (BLOCK, 'Блокировка')
    )

    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    article_uid = models.ForeignKey(Article, db_column='article_uid', on_delete=models.CASCADE, verbose_name='Статья')
    changer_id = models.ForeignKey(User, verbose_name='Автор изменения', db_column='editor_id',
                                   on_delete=models.DO_NOTHING)
    record_date = models.DateTimeField(verbose_name='Дата изменения', auto_now_add=True)
    change_type = models.CharField(verbose_name='Вид изменения', max_length=1024, choices=ARTICLE_STATUSES)

    def __str__(self):
        return f'Статья {self.article_uid.topic}, ' \
               f'автор: {self.article_uid.author_id.email} ' \
               f'изменение {self.change_type} ' \
               f'от {self.record_date}, ' \
               f'автор: {self.changer_id}'

    @receiver(post_save, sender=Article)
    def create_article(sender, instance, created, **kwargs):
        if created:
            ArticleHistory.objects.create(changer_id=instance.author_id, article_uid=instance, change_type='Создание')
        else:
            if instance.blocked:
                ArticleHistory.objects.create(changer_id=instance.author_id, article_uid=instance,
                                              change_type='Удаление')
            else:
                ArticleHistory.objects.create(changer_id=instance.author_id, article_uid=instance,
                                              change_type='Редактирование')

    class Meta:
        indexes = [models.Index(fields=['change_type'])]
        verbose_name = "История статьи"
        verbose_name_plural = "История статей"
        db_table = 'article_history'


class Comment(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    article_uid = models.ForeignKey(Article, related_name='Статья', on_delete=models.CASCADE, verbose_name='Статья')
    user_id = models.ForeignKey(User, related_name='Автор', on_delete=models.DO_NOTHING, null=True,
                                verbose_name='Автор')
    body = models.TextField(default='ici', null=False, verbose_name='Содержимое')
    date_added = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    time_added = models.TimeField(auto_now_add=True, db_index=True, verbose_name='Время добавления')

    def __str__(self):
        return f'{self.article_uid.topic} {self.user_id.username}'

    @staticmethod
    def count(guid):
        return Comment.objects.filter(article_uid=guid).count()

    class Meta:
        ordering = ['date_added', 'time_added']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        db_table = 'comment'


class CommentComment(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    comment_uid = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                    verbose_name='Комментарий')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                verbose_name='Автор')
    body = models.TextField(default='ici', null=False, verbose_name='Содержимое')
    date_added = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')
    time_added = models.TimeField(auto_now_add=True, db_index=True, verbose_name='Время добавления')

    def __str__(self):
        return f'{self.comment_uid.article_uid.topic} {self.user_id.username}'

    @staticmethod
    def count(guid):
        return CommentComment.objects.filter(comment_uid=guid).count()

    class Meta:
        ordering = ['comment_uid', 'date_added', 'time_added']
        verbose_name = "Комментарий для комментария"
        verbose_name_plural = "Комментарии для комментариев"
        db_table = 'comment_for_comment'


class ArticleLike(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    date_added = models.DateField(default=timezone.now, verbose_name='Дата создания', db_column='dts')
    article_uid = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    event_counter = models.IntegerField(verbose_name='Счетчик', default=1, null=False)

    @staticmethod
    def count(guid):
        return ArticleLike.objects.filter(article_uid=guid).count()

    @staticmethod
    def get_like_type(article, user):
        try:
            obj = ArticleLike.objects.filter(article_uid=article, user_id=user).first()
            if obj:
                return "dislike" if obj.event_counter == 1 else "like"
            return "like"
        except:
            return "like"

    @staticmethod
    def get_like_rating(user):
        try:
            rating = ArticleLike.objects.filter(
                article_uid__in=[x.guid for x in Article.objects.filter(author_id=user)]).aggregate(
                Sum('event_counter')).get('event_counter__sum', 0)
            return 0 if rating is None else rating
        except Exception as E:
            print(f'Error in calculation of article likes: {E}')
            return 0

    @staticmethod
    def set_like(article, user):
        obj = ArticleLike.objects.filter(article_uid=article, user_id=user).first()
        if obj:
            obj.event_counter = 0 if obj.event_counter > 0 else 1
            obj.save()
        else:
            ArticleLike.objects.create(article_uid=article, user_id=user, event_counter=1)

    def like(self):
        self.set_like(self.article_uid, self.user_id)

    class Meta:
        indexes = [models.Index(fields=['date_added'])]
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'article_uid'], name="%(app_label)s_%(class)s_unique")
        ]
        verbose_name = "Лайк (статьи)"
        verbose_name_plural = "Лайки (статей)"
        db_table = 'article_like'


class CommentLike(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    date_added = models.DateField(default=timezone.now, verbose_name='Дата создания', db_column='dts')
    comment_uid = models.ForeignKey(Comment, verbose_name='Статья', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name='Автор', on_delete=models.SET_NULL, null=True)
    event_counter = models.IntegerField(verbose_name='Счетчик', default=1, null=False)

    @staticmethod
    def count(guid):
        return CommentLike.objects.filter(comment_uid=guid).count()

    @staticmethod
    def get_like_rating(user):
        try:
            rating = CommentLike.objects.filter(
                comment_uid__in=[x.guid for x in Comment.objects.filter(user_id=user)]).aggregate(
                Sum('event_counter')).get('event_counter__sum', 0)
            return 0 if rating is None else rating
        except Exception as E:
            print(f'Error in calculation of comment likes: {E}')
            return 0

    @staticmethod
    def get_like_type(comment, user):
        try:
            obj = CommentLike.objects.filter(comment_uid=comment, user_id=user).first()
            if obj:
                return "dislike" if obj.event_counter == 1 else "like"
            return "like"
        except:
            return "like"

    @staticmethod
    def set_like(comment, user):
        obj = CommentLike.objects.filter(comment_uid=comment, user_id=user).first()
        if obj:
            obj.event_counter = 0 if obj.event_counter > 0 else 1
            obj.save()
        else:
            CommentLike.objects.create(comment_uid=comment, user_id=user, event_counter=1)

    def like(self):
        self.set_like(self.comment_uid, self.user_id)

    class Meta:
        indexes = [models.Index(fields=['date_added'])]
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'comment_uid'], name="%(app_label)s_%(class)s_unique")
        ]
        verbose_name = "Лайк (комментария)"
        verbose_name_plural = "Лайки (комментариев)"
        db_table = 'comment_like'


class Notification(models.Model):
    guid = models.CharField(primary_key=True, max_length=64, editable=False, default=uuid.uuid4, db_column='guid',
                            verbose_name='Ключ')
    date_added = models.DateField(default=timezone.now, verbose_name='Дата создания', db_column='dts')
    author_id = models.ForeignKey(User, related_name='Создатель', on_delete=models.CASCADE, verbose_name='Отправитель')
    recipient_id = models.ForeignKey(User, related_name='Получатель', on_delete=models.CASCADE,
                                     verbose_name='Получатель')
    article_uid = models.ForeignKey(Article, verbose_name='Статья', null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=512, null=False, default='', verbose_name='Сообщение')
    message_readed = models.BooleanField(default=False, verbose_name='Прочитано')

    def __str__(self):
        return f'{self.date_added} от {self.author_id}: {self.message} для {self.recipient_id}'

    class Meta:
        indexes = [models.Index(fields=['date_added'])]
        ordering = ['message_readed', '-date_added']
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        db_table = 'notification'

    @receiver(pre_save, sender=ArticleLike)
    def create_notification_like(sender, instance, **kwargs):
        notification = {'author_id': instance.user_id, 'recipient_id': instance.article_uid.author_id,
                        'message': f'поставил(а) лайк вашей статье - {instance.article_uid.topic}.'}
        new_notification = Notification(**notification)
        new_notification.save()

    @receiver(pre_save, sender=CommentLike)
    def create_notification_like(sender, instance, **kwargs):
        notification = {'author_id': instance.user_id, 'recipient_id': instance.comment_uid.user_id,
                        'message': 'поставил(а) лайк вашему комментарию.'}
        new_notification = Notification(**notification)
        new_notification.save()

    @receiver(post_save, sender=Comment)
    def create_notification_comment(sender, instance, **kwargs):
        notification = {'author_id': instance.user_id, 'recipient_id': instance.article_uid.author_id,
                        'article_uid': instance.article_uid, 'message': 'оставил(а) комментарий к вашей статье - '}
        new_notification = Notification(**notification)
        new_notification.save()
