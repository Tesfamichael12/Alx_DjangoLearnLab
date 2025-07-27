from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  published_date = models.DateField()

  class Meta:
    permissions = [
      ("can_view", "Can view books"),
      ("can_create", "Can create books"),
      ("can_edit", "Can edit books"),
      ("can_delete", "Can delete books"),
    ]

  def __str__(self):
    return self.title

class CustomUserManager(BaseUserManager):
  def create_user(self, email, username, date_of_birth, password=None, **extra_fields):
    if not email:
      raise ValueError("The Email field must be set")
    email = self.normalize_email(email)
    user = self.model(email=email, username=username, date_of_birth=date_of_birth, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, username, date_of_birth, password, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    return self.create_user(email, username, date_of_birth, password, **extra_fields)


class CustomUser(AbstractUser):
  date_of_birth = models.DateField(null=True, blank=True)
  profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

  objects = CustomUserManager()

  def __str__(self):
    return self.username
