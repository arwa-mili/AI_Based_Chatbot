from django.db import models
from .base import TimestampedModel

class Language(TimestampedModel):
    language_code = models.CharField(max_length=10, unique=True)
    language_name = models.CharField(max_length=100)
    language_native_name = models.CharField(max_length=100, blank=True, null=True)
    language_direction = models.CharField(max_length=3, choices=[("ltr", "Left-to-Right"), ("rtl", "Right-to-Left")], blank=True, null=True)
    # flag = models.ImageField(upload_to="lang_flags/", blank=True, null=True)

    def __str__(self):
        return self.language_name