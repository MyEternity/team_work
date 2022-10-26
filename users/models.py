from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import settings

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(null=False, unique=True, db_index=True, verbose_name='Электронная почта')
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.username}, ' \
               f'email {self.email}'


class UserProfile(models.Model):
    MALE = 'М'
    FEMALE = 'Ж'
    HIDDEN = 'НД'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (HIDDEN, 'НД')
    )

    userid = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    # firstname = models.CharField(max_length=128, verbose_name='Имя', default='')
    # lastname = models.CharField(max_length=128, verbose_name='Фамилия', default='')
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    birthday = models.DateField(verbose_name='Дата рождения', null=False, default='2001-01-01')
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=5)
    phone_number = models.CharField(max_length=16, verbose_name='Номер телефона')
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
            return settings.MEDIA_URL + ref.profile_image.name if ref.profile_image else '/' + settings.STATIC_URL + 'images/comments-1.png'
        else:
            return '/' + settings.STATIC_URL + 'images/comments-1.png'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(userid=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
