from django.db import models
from django.db.models import Q
from django.core.validators import MinLengthValidator
from core.enums.enums import ModelUsedEnum, SentByEnum
from core.models.conversation import Conversation
from core.models.language import Language
from .base import TimestampedModel


class ConversationLine(TimestampedModel):
    text_ar = models.TextField(
        validators=[MinLengthValidator(4)],
        default= "aaaa"
    )
    text_en = models.TextField(
        validators=[MinLengthValidator(4)],
        default= "aaaa"
    )
    
    text_html_en = models.TextField(
        validators=[MinLengthValidator(4)],
        default= "aaaa"
    )
    
    text_html_ar = models.TextField(
        validators=[MinLengthValidator(4)],
        default= "aaaa"
    )
    
    conversation = models.ForeignKey(
        Conversation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="lines"
    )
    
    
    language = models.ForeignKey(
        Language,
        to_field="language_code",
        db_column="language_code",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="conversation_lines"
    )

    model_used = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.value) for tag in ModelUsedEnum],
        default=ModelUsedEnum.GPT.value
    )

    sent_by = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.value) for tag in SentByEnum],
        default=SentByEnum.USER.value
    )
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(model_used__in=[tag.value for tag in ModelUsedEnum]),
                name="check_model_used_enum"
            ),
            models.CheckConstraint(
                check=Q(sent_by__in=[tag.value for tag in SentByEnum]),
                name="check_sent_by_enum"
            )
        ]

    def __str__(self):
        return f"{self.get_text('en')[:50]}... ({self.language.language_code if self.language else 'unknown'})"

    def get_text(self, lang_code: str = 'en'):
        return getattr(self, f"text_{lang_code}", self.text_en)