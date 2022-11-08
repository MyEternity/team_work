import datetime
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from team_work.settings import MEDIA_URL, STATIC_URL


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(null=False, unique=True, db_index=True, verbose_name='Электронная почта')
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    blocked_until = models.DateField(verbose_name='Заблокирован до', default=datetime.date(2000, 1, 1))
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.username}, ' \
               f'email {self.email}'

    @staticmethod
    def restrict_user(user_id):
        usr = User.objects.get(username=user_id)
        usr.blocked_until = datetime.date.today() + +datetime.timedelta(days=14)
        usr.save()
        return datetime.datetime.strftime(usr.blocked_until, '%Y-%m-%d')

    def is_activation_key_expires(self):
        # функция проверяет, не истек ли срок действия ключа активации
        if now() <= self.activation_key_expires + timedelta(hours=48):
            return False
        else:
            return True

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = 'user'


class UserProfile(models.Model):
    MALE = 'М'
    FEMALE = 'Ж'
    HIDDEN = 'НД'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (HIDDEN, 'НД')
    )

    userid = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE,
                                  verbose_name='Ключ')
    # firstname = models.CharField(max_length=128, verbose_name='Имя', default='')
    # lastname = models.CharField(max_length=128, verbose_name='Фамилия', default='')
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    birthday = models.DateField(verbose_name='Дата рождения', null=False, default='2001-01-01')
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=5)
    phone_number = models.CharField(max_length=16, verbose_name='Номер телефона', blank=True, null=True)
    avatar_image = models.ImageField(upload_to='users_avatar', blank=True, verbose_name='Аватар')
    profile_image = models.ImageField(upload_to='users_photo', blank=True, verbose_name='Фотография')

    def __str__(self):
        return f'{self.userid.username}, ' \
               f'email: {self.userid.email}, ' \
               f'создан: {self.creation_datetime}'

    @staticmethod
    def get_photo(user_id):
        ref = UserProfile.objects.get(userid=user_id)
        if ref:
            return MEDIA_URL + ref.profile_image.name if ref.profile_image \
                else '/' + STATIC_URL + 'images/default_user_avatar.jpg'
        else:
            return '/' + STATIC_URL + 'images/default_user_avatar.jpg'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(userid=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        db_table = 'profile'
