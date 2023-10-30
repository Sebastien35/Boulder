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
        fields = ('title', 'file', 'author')  # Ajoutez 'author' aux champs du formulaire

    def __init__(self, user, *args, **kwargs):
        super(MediaForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user  # Définissez l'utilisateur comme valeur initiale du champ 'author'
        self.fields['author'].widget = forms.HiddenInput()  # Cachez le champ 'author' dans le formulaire

        
class TextPostForm(forms.ModelForm):
    class Meta:
        model = text_post
        fields = ['content']
        widget = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your post here...'})
        }
