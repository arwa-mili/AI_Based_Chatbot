from django.urls import path
from chat.views import ChatView
from chat.views import ConversationView
from chat.views.analyse_detail.views import AnalysisDetailView
from chat.views.analyse_history.views import AnalysisHistoryView
from chat.views.analyse_text.views import AnalyzeTextView
from chat.views.chat.views import ConversationMessagesView
from chat.views.user_summary.views import UserSummaryView



urlpatterns = [
    path('message', ChatView.as_view(), name='chat'),
    path('conversation', ConversationView.as_view(), name='conversation'),
    path('conversations/<int:conversation_id>/messages/', ConversationMessagesView.as_view(), name='conversation-messages'),
   # path('analyze/conversations/', AnalyzeConversationsView.as_view(), name='analyze_conversations'),
    path('analyze/text/', AnalyzeTextView.as_view(), name='analyze_text'),
    
    path('history/', AnalysisHistoryView.as_view(), name='history'),
    path('analysis/<uuid:analysis_id>/', AnalysisDetailView.as_view(), name='detail'),
    
    path('user/summary/', UserSummaryView.as_view(), name='user_summary'),
    
]
