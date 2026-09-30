from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class EmailUserManager(UserManager):
 # Stock UserManager is keyed on username; this one is keyed on email.
 def _create_user(self, email, password, **extra_fields):
  if not email:
   raise ValueError("The email must be set.")
  user = self.model(email=self.normalize_email(email), **extra_fields)
  user.set_password(password)
  user.save(using=self._db)
  return user

 def create_user(self, email, password=None, **extra_fields):
  extra_fields.setdefault('is_staff', False)
  extra_fields.setdefault('is_superuser', False)
  return self._create_user(email, password, **extra_fields)

 def create_superuser(self, email, password=None, **extra_fields):
  extra_fields.setdefault('is_staff', True)
  extra_fields.setdefault('is_superuser', True)
  return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
 username = None
 email = models.EmailField(unique=True)
 # Provider-neutral external identity (currently the Supabase JWT `sub` claim).
 # Nullable so admin/superuser accounts without an external identity don't collide
 # on an empty string; unique already creates the index.
 auth_id = models.CharField(
  max_length=255,
  unique=True,
  db_index=True,
  null=True,
  blank=True,
 )

 USERNAME_FIELD = 'email'
 REQUIRED_FIELDS = []

 objects = EmailUserManager()

 def __str__(self):
  return self.email
