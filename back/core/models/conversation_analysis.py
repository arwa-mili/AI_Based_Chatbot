
from django.db import models
from core.models.user import User
from core.models.conversation import Conversation
from .base import TimestampedModel
import uuid

class ConversationAnalysis(TimestampedModel):
    """Stores analysis results for conversations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversation_analyses"
    )
    
    # Reference to analyzed conversations
    conversations = models.ManyToManyField(
        Conversation,
        related_name="analyses",
        blank=True
    )
    
    # Analysis settings
    output_lang = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('ar', 'Arabic'), ('auto', 'Auto')],
        default='auto'
    )
    
    # Analysis results
    summary_ar = models.TextField(blank=True, default='')
    summary_en = models.TextField(blank=True, default='')
    
    detected_language = models.CharField(max_length=10, default='en')
    question_count = models.IntegerField(default=0)
    avg_msg_length = models.FloatField(default=0.0)
    common_topics = models.JSONField(default=list)
    
    # Statistics
    total_conversations = models.IntegerField(default=0)
    total_interactions = models.IntegerField(default=0)
    total_user_messages = models.IntegerField(default=0)
    total_bot_messages = models.IntegerField(default=0)
    
    # Processing status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, default='')
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Analysis {self.id} - {self.user.email} ({self.status})"
    
    def get_summary(self, lang='en'):
        """Get summary in specified language"""
        if lang == 'ar':
            return self.summary_ar or self.summary_en
        return self.summary_en or self.summary_ar

