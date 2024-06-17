# ---------------- External Imports -----------------#
from django.db import models

# ---------------- Internal Imports -----------------#

# Create your models here.
class CreationModeificationBase(models.Model):
    """Mixin for adding creation and modification datetime."""
    created = models.DateTimeField(auto_now_add=True, help_text="When this instance was created.")
    modified = models.DateTimeField(auto_now=True, help_text="When this instance was modified.")

    class Meta:
        abstract = True