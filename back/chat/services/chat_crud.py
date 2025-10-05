
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.db.models import F 

from core.models.conversation import Conversation
from core.models.conversation_line import ConversationLine

User = get_user_model()



import jwt
from jwt.algorithms import RSAAlgorithm


class AccountNotVerifiedError(Exception):
    """Raised when user account exists but is not verified/active."""

class ConversationService:
    @staticmethod
    def create_conversation(user_id,title_en,title_ar,main_langauge, **extra_fields):
        conv = Conversation(
            user_id=user_id,
            title_en=title_en,
            title_ar=title_ar,
            language_id=main_langauge, 
            **extra_fields
        )
        conv.save()

        # Increment conversations_count atomically
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.filter(id=user_id).update(conversations_count=F('conversations_count') + 1)

        return conv

    @staticmethod
    def get_conversations(pageNumber: int, pageSize: int, user_id: str, language: str, search: str = ""):
        print(language)
        title_field = f"title_{language}"

        queryset = Conversation.objects.filter(user_id=user_id)

        if search:
            queryset = queryset.filter(title_en__icontains=search)

        queryset = queryset.order_by('-updated_at')

        conversations = queryset.annotate(title=F(title_field)).values('id', 'title')

        start = (pageNumber - 1) * pageSize
        end = start + pageSize
        paginated = list(conversations)[start:end]

        return {
            "items": paginated,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
            "totalPages": (len(conversations) + pageSize - 1) // pageSize
        }
        
    @staticmethod
    def get_conversation_messages(
        conversation_id: int,
        pageNumber: int = 1,
        pageSize: int = 10,
        user_id: str = None
    ):
        """
        Get paginated messages for a conversation.
        Each message returns its HTML content based on its own language.
        """
        conversation = Conversation.objects.filter(id=conversation_id, user_id=user_id).first()
        if not conversation:
            raise ValueError("Conversation not found or access denied.")

        queryset = ConversationLine.objects.filter(conversation_id=conversation_id).order_by("created_at")

        total_count = queryset.count()
        total_pages = (total_count + pageSize - 1) // pageSize

        start_index = total_count - pageNumber * pageSize
        end_index = total_count - (pageNumber - 1) * pageSize
        if start_index < 0:
            start_index = 0

        lines = list(queryset[start_index:end_index])

        items = []
        for line in lines:
            lang_code = line.language.language_code if line.language else "en"
            html_field = f"text_html_{lang_code}"
            content = getattr(line, html_field, line.text_en)  

            items.append({
                "id": line.id,
                "text": content,
                "sent_by": line.sent_by,
                "created_at": line.created_at,
                "model_used": line.model_used,
                "language_code": lang_code,
            })

        return {
            "items": items,
            "totalPages": total_pages,
            "pageNumber": pageNumber,
            "pageSize": pageSize,
        }
