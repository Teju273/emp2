from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models


class UserManager(BaseUserManager):
    """
    Creates and saves a user with username, email and password
    """

    def create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff = kwargs['is_staff']
        user.is_active = kwargs['is_active']
        user.is_superuser = kwargs['is_superuser']
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, **kwargs):
        """
        Creates and saves a superuser with username, email and password
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        return user


class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    role = models.ForeignKey(Role, null=True, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=15,null=True, blank=True,  unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', 'role']

    objects = UserManager()

    def __str__(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    emp_id = models.IntegerField(unique=True)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    mgr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', blank=True, null=True)

