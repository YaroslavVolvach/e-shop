from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.utils import timezone
from .manager import CustomUserManager
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django_rest_passwordreset.signals import reset_password_token_created

Gender = (
    ('Not specified', 'Not specified',),
    ('Female', 'Female',),
    ('Male', 'Male',)
)

image = "account_image/default_account_image/Default_avatar_without_gender.png"


class CustomUser(PermissionsMixin, AbstractBaseUser):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=20)

    country = CountryField(null=True, blank=True)
    city = models.CharField(max_length=15, blank=True, default='Not specified')
    date_joined = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=13, choices=Gender,
                              default='Not specified')
    main_image = models.ImageField(default=image, upload_to='account_image/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name

    def get_absolute_url(self):
        return reverse('account:profile_for_staff', args=[self.id])

    @property
    def age(self):
        today = timezone.now()
        birth_date = self.birth_date
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.user_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri('/account/api/password_reset/confirm/'),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('account/account_reset_password.html', context)
    email_plaintext_message = render_to_string('account/account_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
