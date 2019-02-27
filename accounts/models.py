from functools import wraps

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

def disable_for_loaddata(signal_handler):
    """Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if kwargs['raw']:
            return
        signal_handler(*args, **kwargs)
    return wrapper


class Account(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatar_images',
        blank=True,
        null=True,
        verbose_name='Аватар',
        default='avatar_images/default.png')

    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    age = models.IntegerField(
        blank=True,
        null=True,
        default=18,
        verbose_name='Возраст'
    )

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def __str__(self):
        return self.username

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class AccountProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(Account, unique=True, null=False,
                                db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128,
                               blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512,
                               blank=True)
    language = models.TextField(verbose_name='язык', max_length=10,
                                blank=True)
    url = models.TextField(verbose_name='url на google+', max_length=512,
                           blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=Account)
    @disable_for_loaddata
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            AccountProfile.objects.create(user=instance)

    @receiver(post_save, sender=Account)
    @disable_for_loaddata
    def save_user_profile(sender, instance, **kwargs):
        instance.accountprofile.save()
