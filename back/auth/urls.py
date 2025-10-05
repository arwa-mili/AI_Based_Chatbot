from django.urls import path
from auth.views import RegisterView, LoginView, UserProfileView, RefreshTokenView
from chat.views.user_summary.views import UserSummaryView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh-token"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),


]
