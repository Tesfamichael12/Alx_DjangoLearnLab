from django.urls import path
from .views import UserRegistrationView, UserLoginView, FollowUserView, UnfollowUserView, FeedView

urlpatterns = [
  path('register/', UserRegistrationView.as_view(), name='register'),
  path('login/', UserLoginView.as_view(), name='login'),
  path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
  path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
  path('feed/', FeedView.as_view(), name='feed'),
]
