from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = NotificationSerializer

  def get_queryset(self):
    return self.request.user.notifications.all().order_by('-timestamp')
