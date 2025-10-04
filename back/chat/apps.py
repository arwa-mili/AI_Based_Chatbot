from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    
    def ready(self):
        """Load models on app startup"""
        from .services import ModelManager
        try:
            ModelManager()
        except Exception as e:
            print(f"Warning: Could not load ML models on startup: {e}")

