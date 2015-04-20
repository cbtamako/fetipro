# encoding=utf-8

import twitter
from urllib import request
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.cache import cache
from social.apps.django_app.default.models import UserSocialAuth
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField("ユーザー名", max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    display_name = models.CharField("表示名", max_length=30, blank=True)
    email = models.EmailField("メールアドレス", blank=True)
    is_staff = models.BooleanField("スタッフ権限", default=False)
    is_active = models.BooleanField("有効", default=True)
    created_at = models.DateTimeField("新規登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    feties = models.ManyToManyField("master.Feti", through='UserFeti')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['display_name']

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.username

    def get_twitter_account(self):
        try:
            account = UserSocialAuth.objects.get(user=self, provider="twitter")
        except UserSocialAuth.DoesNotExist:
            return None

        user = cache.get("tw_uid_{0}".format(account.uid))
        if user is False:
            return None
        if user:
            return user

        api = twitter.Twitter(auth=twitter.OAuth(
                                                 settings.SOCIAL_AUTH_TWITTER_ACCESS_KEY, settings.SOCIAL_AUTH_TWITTER_ACCESS_SECRET,
                                                 settings.SOCIAL_AUTH_TWITTER_KEY, settings.SOCIAL_AUTH_TWITTER_SECRET
                                                 ))
        user = api.users.show(user_id=account.uid)
        if user:
            url = user.get("url")
            if url:
                try:
                    with request.urlopen(url) as response:
                        user["url"] = url = response.geturl()
                except: pass

            url = user.get("profile_image_url")
            if url:
                user["profile_image_url"] = url.replace("_normal", "")

            url = user.get("profile_image_url_https")
            if url:
                user["profile_image_url_https"] = url.replace("_normal", "")

            cache.set("tw_uid_{0}".format(account.uid), user)
        else:
            cache.set("tw_uid_{0}".format(account.uid), False)
        return user


class UserFeti(models.Model):

    class Status(object):
        Yes = 1
        No = 0
        Non = -1

    user = models.ForeignKey(User)
    feti = models.ForeignKey("master.Feti")
    created_at = models.DateTimeField("新規登録日時", auto_now_add=True)
    updated_at = models.DateTimeField("最終更新日時", auto_now=True)

    STATUS_CHOICES = (
                      (Status.Yes, "はい"),
                      (Status.No, "いいえ"),
                      (Status.Non, "未回答")
                      )
    status = models.IntegerField("状態", choices=STATUS_CHOICES)

    @property
    def is_non(self):
        return self.status == self.Status.Non

    @property
    def is_yes(self):
        return self.status == self.Status.Yes

    @property
    def is_no(self):
        return self.status == self.Status.No


