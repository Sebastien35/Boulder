from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import RegistrationForm, MediaForm, TextPostForm
from .models import Media, text_post

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect the user to another page after successful login.
                return redirect('home')
            else:
                messages.error(request, 'Identifiants incorrects')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']
            user.save()
            return redirect('login')  # Redirect the user to the login page after successful registration.
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            media_form = MediaForm(request.POST, request.FILES)
            if media_form.is_valid():
                media_form.save()
       
            else:
                text_post_form = TextPostForm(request.POST)
            if text_post_form.is_valid():
                text_post_form.save()
            
            else:
                media_form = MediaForm()
                text_post_form = TextPostForm()

    media_list = Media.objects.all()
    text_posts = text_post.objects.all()

    context = {
        'media_form': MediaForm,
        'text_post_form': TextPostForm,
        'media_list': media_list,
        'text_posts': text_posts,
    }

    return render(request, 'home.html', context)

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.user, request.POST, request.FILES)  # Passez l'utilisateur actuellement connecté
        if form.is_valid():
            media = form.save(commit=False)
            media.author = request.user  # Utilisez request.user pour obtenir l'objet d'utilisateur actuellement connecté
            media.save()
            return redirect('home')
    else:
        form = MediaForm()
    return render(request, 'upload_media.html', {'form': form})