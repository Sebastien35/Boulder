from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from .forms import RegistrationForm, MediaForm, TextPostForm
from .models import Media, text_post



def register(request):
    error_message = None
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte automatiquement l'utilisateur après l'inscription
            return redirect('home')  # Redirige vers la page d'accueil après l'inscription
        else:
            error_message = 'Erreur dans le formulaire'
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home_view(request):
    if request.method == 'POST':
        user = request.user  # Récupérez l'utilisateur connecté

        # Passez l'utilisateur au formulaire MediaForm lors de l'initialisation
        media_form = MediaForm(user=user, data=request.POST, files=request.FILES)
        text_post_form = TextPostForm(request.POST)

        if media_form.is_valid() and 'file' in request.FILES:
            media_form.save()
        elif text_post_form.is_valid():
            text_post_form.save()

    else:
        # Si la méthode de la requête est GET, initialisez le formulaire sans l'utilisateur
        media_form = MediaForm()  # Ne passez pas l'utilisateur ici pour les requêtes GET
        text_post_form = TextPostForm()

    media_list = Media.objects.all()
    text_posts = text_post.objects.all()

    context = {
        'media_form': media_form,
        'text_post_form': text_post_form,
        'media_list': media_list,
        'text_posts': text_posts,
    }

    return render(request, 'home.html', context)

@login_required
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Le formulaire s'occupera d'ajouter l'auteur automatiquement
            return redirect('home')
    else:
        form = MediaForm()  # Initialisez le formulaire sans aucun argument

    return render(request, 'upload_media.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        # Votre logique de vérification de formulaire ici
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigez l'utilisateur vers la page d'accueil après la connexion réussie
                return redirect('home')  # Assurez-vous d'avoir un nom d'URL nommé 'home' pour votre page d'accueil
            else:
                messages.error(request, 'Identifiants incorrects')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class CustomLoginView(LoginView):
    redirect_authenticated_user = True  # Rediriger les utilisateurs déjà connectés vers la page spécifiée

    def get_success_url(self):
        return reverse_lazy('home')