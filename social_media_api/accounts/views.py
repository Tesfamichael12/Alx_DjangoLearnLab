from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions  # Import permissions module
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from posts.serializers import PostSerializer
from posts.models import Post


class UserRegistrationView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for following another user
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Exact line as required
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.following.add(user_to_follow)
        return Response(
            {"detail": "User followed successfully"}, status=status.HTTP_200_OK
        )


# View for unfollowing a user
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Exact line as required
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": "User unfollowed successfully"}, status=status.HTTP_200_OK
        )


# View for showing the feed with posts from followed users
class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Exact line as required
    queryset = CustomUser.objects.all()

    def get(self, request):
        followed_users = request.user.following.all()
        posts = Post.objects.filter(author__in=followed_users).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
