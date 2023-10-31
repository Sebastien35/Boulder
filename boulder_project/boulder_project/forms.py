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
        fields = ('title', 'file', 'author')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MediaForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['author'].initial = user
            self.fields['author'].widget = forms.HiddenInput()

    def save(self, commit=True, *args, **kwargs):
        # Surchargez la méthode save pour ajouter l'auteur au modèle Media
        instance = super(MediaForm, self).save(commit=False, *args, **kwargs)
        if commit:
            instance.author = self.fields['author'].initial
            instance.save()
        return instance
        
class TextPostForm(forms.ModelForm):
    class Meta:
        model = text_post
        fields = ['content']
        widget = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here...'})
        }
