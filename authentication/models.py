from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, firstname and password.
        """
        if email == "":
            raise ValueError("Users must have an email address")
        # elif first_name == "":
        #     raise ValueError("Users must have a firstname")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        """
        Creates and saves a superuser with the given email,
        firstname and password.
        """
        user = self.create_user(
            self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Staff(AbstractBaseUser, PermissionsMixin):
    '''A class to represent a Staff.'''
    class Roles(models.TextChoices):
        SALES = "SALES", "sales"
        SUPPORT = "SUPPORT", "support"
        MANAGEMENT = "MANAGEMENT", "management"

    role = models.CharField(max_length=25, choices=Roles.choices,
                            # Default staff is manager
                            default=Roles.SUPPORT)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(
        verbose_name="email address",
        max_length=100,
        unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
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

    # return the staff if he's in a list
    def __repr__(self):
        return self.__str__()

    def has_perm(self, perm, obj=None):
        # print('perm', perm, 'object', obj)
        if (perm == 'authentication.add_staff' or
                perm == 'authentication.change_staff' or
                perm == 'authentication.delete_staff'):
            return self.is_manager
        return True

    def has_module_perms(self, app_label):
        # print('app module', app_label)
        # access to staff forbidden if not admin
        if app_label == 'authentication':
            if self.is_admin:
                return True
            else:
                return False
        return True

    def save(self, *args, **kwargs):
        if not self.role or self.role is None:
            self.type = Staff.Roles.MANAGEMENT
        return super().save(*args, **kwargs)

    @property
    def is_seller(self):
        if self.role == self.Roles.SALES:
            return True
        else:
            return False

    @property
    def is_support(self):
        if self.role == self.Roles.SUPPORT:
            return True
        else:
            return False

    @property
    def is_manager(self):
        if self.role == self.Roles.MANAGEMENT:
            return True
        else:
            return False
