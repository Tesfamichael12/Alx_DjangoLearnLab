from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


# Custom user manager
class CustomUserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    """
    Creates and saves a User with the given email and password.
    """
    if not email:
      raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extra_fields):
    """
    Creates and saves a superuser with the given email and password.
    """
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self.create_user(email, password, **extra_fields)


# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_('email address'), unique=True)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=30, blank=True)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(auto_now_add=True)

  # Avoiding reverse accessor clashes with auth.User
  groups = models.ManyToManyField(
    Group,
    related_name="customuser_set",  # Added related_name to avoid clash
    blank=True,
    help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
    related_query_name="customuser",
  )
  user_permissions = models.ManyToManyField(
    Permission,
    related_name="customuser_permissions_set",  # Added related_name to avoid clash
    blank=True,
    help_text=_('Specific permissions for this user.'),
    related_query_name="customuser_permissions",
  )

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email


# Example model for the API
class Author(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name


class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  publication_year = models.IntegerField()

  def __str__(self):
    return self.title
