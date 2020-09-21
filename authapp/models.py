from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mainapp.models import ProductCategory, Product


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', verbose_name='аватар', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст', default=18)
    email = models.CharField(verbose_name='e-mail', max_length=100)

    MALE = True
    FEMALE = False
    GENDER_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female')
    ]
    gender = models.BooleanField(verbose_name='пол', choices=GENDER_CHOICES, default=True)

    RUSSIA = 'Ru'
    UKRAINE = 'Ukr'
    CHINA = 'Ch'
    COUNTRY_CHOICES = [
        (RUSSIA, 'Russia'),
        (UKRAINE, 'Ukraine'),
        (CHINA, 'China'),
    ]
    country = models.CharField(verbose_name='страна', max_length=100, choices=COUNTRY_CHOICES, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(datetime.now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) >= self.activation_key_expires:
            return True
        else:
            return False


class ShopUserProfile(models.Model):
    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=128, verbose_name='теги', blank=True)
    about_me = models.TextField(max_length=512, verbose_name='о себе', blank=True)
    social_url = models.CharField(max_length=128, verbose_name='ссылка на соц.сети', blank=True)
    language = models.CharField(max_length=100, verbose_name='язык', blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
