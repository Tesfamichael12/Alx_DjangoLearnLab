from rest_framework import viewsets, generics, status
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification  # Import Notification model

# Post view for handling posts CRUD operations
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Comment view for handling comments CRUD operations
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# View for showing the feed with posts from followed users
class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get the users that the current user is following
        following_users = request.user.following.all()  

        # Fetch posts from the users that the current user is following, ordered by creation date
        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")

        # Serialize the posts and return them
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# View for liking a post
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):  # Updated pk instead of post_id
        # Use generics.get_object_or_404 to fetch the post instance
        post = generics.get_object_or_404(Post, pk=pk)  # Updated to match the expected pattern
        
        # Create or get the Like object
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # If a new like was created, create a notification
            Notification.objects.create(
                recipient=post.author,  # Post author receives the notification
                actor=request.user,  # The user who liked the post
                verb='liked',  # Action performed
                target=post  # The post that was liked
            )
            return Response({"detail": "Post liked successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

# View for unliking a post
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):  # Updated pk instead of post_id
        # Use generics.get_object_or_404 to fetch the post instance
        post = generics.get_object_or_404(Post, pk=pk)  # Updated to match the expected pattern
        
        # Check if the like exists
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()  # Remove the like
            return Response({"detail": "Post unliked successfully"}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"detail": "You have not liked this post"}, status=status.HTTP_400_BAD_REQUEST)
