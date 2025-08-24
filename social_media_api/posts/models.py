from django.db import models
from django.conf import settings

# Post model remains unchanged
class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
  title = models.CharField(max_length=255)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

# Comment model remains unchanged
class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'Comment by {self.author} on {self.post}'

# New Like model
class Like(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'post')  # Ensure a user can like a post only once

  def __str__(self):
    return f'{self.user} liked {self.post}'
