from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class Userposts(models.Model):
    image = models.ImageField(upload_to="images/")

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class UserProfile(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True 

class Passport(models.Model):
    type = models.CharField(max_length=2)
    issuing_country = models.CharField(max_length=3)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=20)
    nationality = models.CharField(max_length=3)
    dob = models.CharField(max_length=10)
    sex = models.CharField(max_length=1)
    doe = models.CharField(max_length=10)

    def _str_(self):
        return f"{self.Surname}, {self.Name}"

