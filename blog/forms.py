from django import forms
from django.forms import ModelForm
from .models import Post, Comment, ContactMethod


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']


class ContactMethodForm(forms.ModelForm):
    class Meta:
        model = ContactMethod
        exclude = []
