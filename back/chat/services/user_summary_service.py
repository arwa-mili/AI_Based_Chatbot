from django.utils import timezone
from core.models.user import User
from chat.services.model import ChatAnalyzerService
from core.models.conversation import Conversation

class UserSummaryService:
    """
    Service for retrieving or triggering a user's conversation summary.
    """

    def __init__(self):
        self.analyzer = ChatAnalyzerService()

    def get_user_summary(self, user: User, lang_code: str = 'en') -> dict:
        """
        If the user's conversation quota is reached and no summary has been generated,
        automatically trigger summarization for the last conversations.
        Otherwise, return the existing summary data.
        """
        # Case 1: Trigger summarization
        if user.conversations_count >= user.conversations_quota and not user.last_summary_generated:
            last_conversations = self._get_recent_conversations(user)

            if not last_conversations:
                return {
                    "success": False,
                    "info": "NO_CONVERSATIONS_FOUND",
                    "summary": "",
                    "last_updated": None,
                    "language": lang_code,
                }

            # Trigger summarization
            analysis = self.analyzer.analyze_conversations(
                conversation_ids=[conv.id for conv in last_conversations],
                user=user,
                output_lang=lang_code
            )

            # Reset user fields after summarization
            user.last_summary_generated = True
            user.conversations_count = 0
            user.last_analysis_date = timezone.now()
            user.save(update_fields=['last_summary_generated', 'conversations_count', 'last_analysis_date'])

            # Return generated summary
            summary = analysis.summary_en if lang_code == 'en' else analysis.summary_ar
            return {
                "success": True,
                "summary": summary,
                "last_updated": user.last_analysis_date,
                "language": lang_code,
                "triggered": True
            }

        # Case 2: Just return the last saved summary
        else:
            summary = user.last_analysis_summary_en if lang_code == 'en' else user.last_analysis_summary_ar
            return {
                "success": True,
                "summary": summary,
                "last_updated": user.last_analysis_date,
                "language": lang_code,
                "triggered": False
            }

    def _get_recent_conversations(self, user: User):
        """Fetch the most recent conversations of the user."""
        return Conversation.objects.filter(user=user).order_by('-created_at')[:user.conversations_quota]
