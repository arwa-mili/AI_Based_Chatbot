from django.apps import AppConfig
from .services.model import ModelManager


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    
    def ready(self):
        """Load models on app startup"""
        try:
            ModelManager()
        except Exception as e:
            print(f"Warning: Could not load ML models on startup: {e}")

