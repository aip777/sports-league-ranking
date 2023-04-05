from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
from django.contrib.auth.models import Group


class UserManger(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an email')
        user = self.model(
            email=self.normalize_email(email),
        )
        # group = Group.objects.all()
        # user.groups.add(group)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractUser):
    username = models.CharField(max_length=55)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(verbose_name='admin', default=False)
    is_superuser = models.BooleanField(default=False)

    # notice the absence of a "Password field", that is built in.

    objects = UserManger()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = 'User'

# Group.add_to_class('description', models.CharField(max_length=180, null=True, blank=True))
# Group.add_to_class('created_by', models.ForeignKey(CustomUserModel, on_delete=models.DO_NOTHING, null=True, blank=True))