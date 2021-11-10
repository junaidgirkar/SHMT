from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name, 
            last_name=last_name,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.staff = True
        user.save(using=self._db)
        return user
    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email       = models.EmailField(max_length=255, unique=True, default="")
    first_name  = models.CharField(max_length=64, default="")
    last_name   = models.CharField(max_length=64, default="")
    
    active      = models.BooleanField(default=True)
    staff       = models.BooleanField(default=False)
    admin       = models.BooleanField(default=False)

    objects     = UserManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

def save_user(instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)   

post_save.connect(save_user, sender=settings.AUTH_USER_MODEL)
