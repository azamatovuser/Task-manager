from django.urls import path
from apps.account.views import (TopAccountAPIList,
                                AccountAPIDetail,
                                AccountListAPIView,
                                FriendRemoveAPIView,
                                FriendAddAPIView,
                                AccountRegisterView,
                                LoginView)

urlpatterns = [
    path("top_accounts/", TopAccountAPIList.as_view()),
    path("detail/<int:pk>/", AccountAPIDetail.as_view()),
    path("all_accounts/", AccountListAPIView.as_view()),
    path("friend_remove/<int:pk>/", FriendRemoveAPIView.as_view()),
    path("friend_add/", FriendAddAPIView.as_view()),
    path("register/", AccountRegisterView.as_view()),
    path("login/", LoginView.as_view()),
]