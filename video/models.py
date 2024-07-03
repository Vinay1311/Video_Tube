# ---------------- External Imports -----------------#
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.timezone import now
from django.core.validators import RegexValidator

# ---------------- Internal Imports -----------------#
from helper.models import CreationModeificationBase