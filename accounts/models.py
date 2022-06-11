from random import choice
import string

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings

from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email должен быть определен")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def create_activation_code(self):

        l = "".join([choice(string.ascii_lowercase + string.digits) for i in range(6)])
        self.activation_code = l
        self.save()
    
    @classmethod
    def user_saved(cls, sender, instance, **kwargs):
        if getattr(instance, '_set_password', False):
            instance.auth_token.delete()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        'Сброс пароля',
        reset_password_token.key,
        settings.EMAIL_HOST_USER,
        [reset_password_token.user.email]
        )

@receiver(post_password_reset)
def password_reset_post(user, *args, **kwargs):
    user.auth_token.delete()