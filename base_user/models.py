# ---------------- External Imports -----------------#
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now
from django.core.validators import RegexValidator


# ---------------- Internal Imports -----------------#
from helper import regex_validator
from helper import messages
# Create your models here.
class UserManager(BaseUserManager):
    """Custom user model manager."""
    def _create_user(self, email, password, is_superuser, is_staff, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        current = now()
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=current,
            date_joined=current,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    def create_staff_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, True, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[regex_validator.email_regex])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.email)
    

#     def _create_user(self, email, password, is_superuser, is_staff, **extra_fields):
#         if not email :
#             raise ValueError("Mobile number is required")
#         current = now()
#         user = self.model(
#             email = email,
#             is_staff = is_staff,
#             is_active = True,
#             is_superuser = is_superuser,
#             last_login = current,
#             date_joined = current,
#             **extra_fields

#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_user(self, email = None, password = None, **extra_fields):
#         self.set_password(password)
#         self.save(using=self._db)
#         return self._create_user(email, password, False, False, **extra_fields)
    
#     def create_staff_user(self, email, password = None, **extra_fields):
#         return self._create_user(email, password, True, False, **extra_fields)
    
#     def create_superuser(self, email, password, **extra_fields):
#         user = self._create_user(email, password, True, True, **extra_fields)
#         user.save(using=self._db)
#         return user
    


# # ------ Custom User Model ------- #
    
# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True, validators= [regex_validator.email_regex])
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     last_login = models.DateTimeField(null=True, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
    

#     USERNAME_FIELD = 'email' 
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     def __str__(self):
#         return str(self.email)
