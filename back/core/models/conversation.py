from django.db import models
from core.models.language import Language
from core.models.user import User
from .base import TimestampedModel

class Conversation(TimestampedModel):
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversations"
    )
    title_ar = models.CharField(max_length=100,default= "")
    title_en = models.CharField(max_length=100,default= "")


    def __str__(self):
        return f"{self.title} ({self.main_language})"
