from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
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
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Automatically log in the user after registration if desired.
            # login(request, user)
            return redirect('login')  # Redirect the user to the login page after successful registration.
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def home_view(request):
    if request.method == 'POST':
        # Check if the request contains media file data
        if 'file' in request.FILES:
            media_form = MediaForm(request.POST, request.FILES)
            if media_form.is_valid():
                # Process media form data here
                media_form.save()
                return redirect('home')
            else:
                text_post_form = TextPostForm()  # Create an empty text post form
        else:
            # If no media file is uploaded, assume it's a text post
            text_post_form = TextPostForm(request.POST)
            if text_post_form.is_valid():
                # Process text post form data here
                text_post_form.save()
                return redirect('home')
            else:
                media_form = MediaForm()  # Create an empty media form
    else:
        # If it's a GET request, create empty forms
        media_form = MediaForm()
        text_post_form = TextPostForm()

    # Retrieve media objects and text posts from the database
    media_list = Media.objects.all()
    text_posts = text_post.objects.all()

    context = {
        'media_form': media_form,
        'text_post_form': text_post_form,
        'media_list': media_list,
        'text_posts': text_posts,  # Pass the retrieved text posts to the template
    }
    return render(request, 'home.html', context)

def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('home')  # Redirect to the home page after successful upload
    else:
        form = MediaForm()  # If it's a GET request, create a new empty form
    
    return render(request, 'upload_media.html', {'form': form})