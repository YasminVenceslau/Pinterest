from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Profile, Pin
from .forms import PinForm, SignUpForm, ProfilePicForm

# Página inicial: feed de pins
def home(request):
    pins = Pin.objects.all().order_by("-created_at")
    if request.user.is_authenticated:
        form = PinForm(request.POST or None, request.FILES or None)
        if request.method == "POST" and form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user
            pin.save()
            messages.success(request, "Seu Pin foi postado com sucesso!")
            return redirect('home')
        return render(request, 'home.html', {"pins": pins, "form": form})
    else:
        return render(request, 'home.html', {"pins": pins})


# Lista de perfis
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.warning(request, "Você precisa estar logado para ver os pins.")
        return redirect('home')


# Seguir / deixar de seguir
def follow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.add(profile)
        request.user.profile.save()
        messages.success(request, f"Agora você segue {profile.user.username}!")
        return redirect(request.META.get("HTTP_REFERER"))
    messages.warning(request, "Faça login para seguir usuários.")
    return redirect('home')

def followers(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        followers_list = profile.followed_by.all()  # todos que seguem este perfil
        return render(request, "followers.html", {"profile": profile, "followers": followers_list})
    messages.warning(request, "Faça login para ver os seguidores.")
    return redirect('home')

# Lista de quem o usuário segue
def follows(request, pk):
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user_id=pk)
        follows_list = profile.follows.all()  # todos que este perfil segue
        return render(request, "follows.html", {"profile": profile, "follows": follows_list})
    messages.warning(request, "Faça login para ver os perfis seguidos.")
    return redirect('home')

def unfollow(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        request.user.profile.follows.remove(profile)
        request.user.profile.save()
        messages.success(request, f"Você deixou de seguir {profile.user.username}.")
        return redirect(request.META.get("HTTP_REFERER"))
    messages.warning(request, "Faça login para deixar de seguir.")
    return redirect('home')


# Perfil do usuário
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        pins = Pin.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            action = request.POST.get('follow')
            current_user_profile = request.user.profile
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile, "pins": pins})
    else:
        messages.warning(request, "Você precisa estar logado para ver perfis.")
        return redirect('home')


# Curtir / descurtir Pin
def pin_like(request, pk):
    if request.user.is_authenticated:
        pin = get_object_or_404(Pin, id=pk)
        if pin.likes.filter(id=request.user.id).exists():
            pin.likes.remove(request.user)
        else:
            pin.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    messages.warning(request, "Não está Logado para poder dar Like")
    return redirect('home')


# Excluir Pin
def delete_pin(request, pk):
    if request.user.is_authenticated:
        pin = get_object_or_404(Pin, id=pk)
        if request.user == pin.user:
            pin.delete()
            messages.success(request, "Pin excluído!")
        else:
            messages.error(request, "Você não pode excluir este Pin.")
        return redirect(request.META.get("HTTP_REFERER"))
    messages.warning(request, "Faça login para excluir pins.")
    return redirect('home')


# Editar Pin
def edit_pin(request, pk):
    if request.user.is_authenticated:
        pin = get_object_or_404(Pin, id=pk)
        if request.user == pin.user:
            form = PinForm(request.POST or None, request.FILES or None, instance=pin)
            if request.method == "POST" and form.is_valid():
                form.save()
                messages.success(request, "Pin atualizado com sucesso!")
                return redirect('home')
            return render(request, 'edit_pin.html', {'pin': pin, 'form': form})
        messages.error(request, "Você não pode editar este Pin.")
        return redirect('home')
    messages.warning(request, "Faça login para continuar.")
    return redirect('home')


# Login / Logout / Cadastro
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login efetuado com sucesso!")
            return redirect('home')
        messages.error(request, "Usuário ou senha incorretos.")
        return redirect('login')
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('home')


def register_user(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Cadastro realizado com sucesso!")
        return redirect('home')
    return render(request, "register.html", {"form": form})


# Atualizar perfil
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)
        user_form = SignUpForm(request.POST or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect('home')

        return render(request, "update_user.html", {
            'user_form': user_form,
            'profile_form': profile_form
        })
    else:
        messages.warning(request, "Faça login para editar seu perfil.")
        return redirect('home')

