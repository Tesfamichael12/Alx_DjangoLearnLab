from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from taggit.models import Tag


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()  # Make sure TaggableManager is included here for tags

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_posts_by_tag(tag_slug):
        """Utility method to filter posts by a specific tag slug."""
        try:
            tag = Tag.objects.get(slug=tag_slug)
            return Post.objects.filter(tags__in=[tag])
        except Tag.DoesNotExist:
            return Post.objects.none()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]  # Orders comments by creation date (oldest first)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
