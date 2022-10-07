from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(null=False, unique=True, db_index=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)


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
    creation_datetime = models.DateTimeField(auto_now_add=True)
    birthday = models.DateField(verbose_name='Дата рождения', null=False, default='2001-01-01')
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    gender = models.CharField(verbose_name='Пол', choices=GENDER_CHOICES, blank=True, max_length=5)
    phone_number = models.CharField(max_length=16)
    avatar_image = models.ImageField(upload_to='users_avatar', blank=True)
    profile_image = models.ImageField(upload_to='users_photo', blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(userid=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
