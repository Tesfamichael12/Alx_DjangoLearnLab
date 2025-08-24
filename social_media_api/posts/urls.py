from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView  # Import LikePostView and UnlikePostView

# Set up a router for posts and comments
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# Define the URL patterns
urlpatterns = [
  path('', include(router.urls)),  # Routes for posts and comments
  path('feed/', FeedView.as_view(), name='feed'),  # Add feed route
  path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),  # Updated: pk for post ID
  path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),  # Updated: pk for post ID
]

