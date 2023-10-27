from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Media, text_post


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ('title', 'file')


class TextPostForm(forms.ModelForm):
    class Meta:
        model = text_post
        fields = ['content']
        widget = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here...'})
        }
