from django.urls import path
from chat.views import ChatView
from chat.views import ConversationView
from chat.views.analyse_history.views import AnalysisHistoryView
from chat.views.chat.views import ConversationMessagesView
from chat.views.generate_conversation_title.views import ConversationTitleView
from chat.views.user_summary.views import UserSummaryView



urlpatterns = [
    path('message', ChatView.as_view(), name='chat'),
    path('conversation', ConversationView.as_view(), name='conversation'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
    # path('analyze/conversations/', AnalyzeConversationsView.as_view(), name='analyze_conversations'),
    # path('analyze/text/', AnalyzeTextView.as_view(), name='analyze_text'),
    path('user-summary/', UserSummaryView.as_view(), name='user_summary'),
    path('conversations/<int:conversation_id>/title', ConversationTitleView.as_view(), name='conversation-title'),
    path('summary-history/', AnalysisHistoryView.as_view(), name='history'),
    
    
]
