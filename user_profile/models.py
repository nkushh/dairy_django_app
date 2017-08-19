from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

# Create your models here.
# class CustomUserManager(BaseUserManager):
# 	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
# 		now = timezone.now

# 		if not email:
# 			raise ValueError('The given email must be set')
# 		email = self.normalize_email(email)
# 		user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, 
# 				date_joined=now, **extra_fields)
# 		user.set_password(password)
# 		user.save(using=self._db)
# 		return user

# 	def create_user(self, email, password=None, **extra_fields):
# 		return self._create_user(username, email, password, False, False, **extra_fields)

# 	def create_superuser(self, email, password=None, **extra_fields):
# 		return self._create_user(username, email, password, True, True, **extra_fields)


class User(AbstractBaseUser):
	username = models.CharField(max_length=20, unique=True, db_index=True)
	email = models.EmailField(unique=True)
	joined_on = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'

	# objects = CustomUserManager()

	def __str__(self):
		return self.username
