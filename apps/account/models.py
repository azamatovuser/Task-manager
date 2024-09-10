from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as lazy
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if username is None:
            raise TypeError(lazy("Where is username?"))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        if password is None:
            raise TypeError(lazy("Where is password?"))

        user = self.create_user(
            username=username,
            password=password,
            **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=221, unique=True, db_index=True)
    full_name = models.CharField(max_length=221)
    image = models.ImageField(upload_to='account_images/', null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.username

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return data

class Friend(models.Model):
    user = models.ForeignKey(Account, related_name='friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(Account, related_name='friends_with', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure that the combination of user and friend is unique in one direction
        unique_together = (
            ('user', 'friend'),
        )

    def clean(self):
        # Ensure a user cannot befriend themselves
        if self.user == self.friend:
            raise ValidationError('You cannot add yourself as a friend.')

        # Check for existing friendships in either direction
        if Friend.objects.filter(
            Q(user=self.user, friend=self.friend) |
            Q(user=self.friend, friend=self.user)
        ).exists():
            # Raise a single validation error with a clear message
            raise ValidationError('Friendship already exists.')

    def save(self, *args, **kwargs):
        # Perform clean method validation before saving
        self.clean()
        super().save(*args, **kwargs)
