from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, firstname and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        elif not first_name:
            raise ValueError("Users must have a firstname")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None):
        """
        Creates and saves a superuser with the given email,
        firstname and password.
        """
        user = self.create_user(
            self.normalize_email(email),
            first_name=first_name,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Staff(AbstractBaseUser, PermissionsMixin):
    TYPE_CHOICES = (
        # first is displayed and second in database
        ('Sales', 'sales'),
        ('Support', 'support'),
        ('Management', 'management'),
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(
        verbose_name="email address",
        max_length=100,
        unique=True)
    role = models.CharField(max_length=25, choices=TYPE_CHOICES)
    phone = models.CharField(max_length=20, null=True)
    mobile = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    picture_url = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
