from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagField, TagWidget  # Import TagField and TagWidget

class CustomUserCreationForm(UserCreationForm):
  email = forms.EmailField(required=True)
  class Meta:
    model = User
    fields = ("username", "email", "password1", "password2")


class UserProfileForm(forms.ModelForm):
  email = forms.EmailField(required=True)
  class Meta:
    model = User
    fields = ("username", "email")


class PostForm(forms.ModelForm):
  tags = TagField(required=False)
  class Meta:
    model = Post
    fields = ["title", "content", "tags"]  # Include 'tags' field
    widgets = {
      "tags": TagWidget(),  # Use TagWidget for 'tags' field
    }

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ["content"]
    widgets = {
      "content": forms.Textarea(
        attrs={"rows": 3, "placeholder": "Add a comment..."}
      ),
    }
