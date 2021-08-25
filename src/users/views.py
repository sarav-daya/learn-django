from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import Profile

from users.forms import CustomUserCreationForm

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description__exact="")
    context = {
        "profile": profile,
        "top_skills": top_skills,
        "other_skills": other_skills,
    }
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {
        "profile": profile,
        "skills": skills,
        "projects":projects,
    }
    return render(request, "users/account.html", context)


def login_page(request):

    if request.user.is_authenticated:
        return redirect("profiles")

    context = {}

    if request.method == "POST":
        print(request.user)
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid username or password")
            return render(request, "users/login_register.html", context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login_register.html", context)


def logout_page(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect("login")


def register_user(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect("profiles")
        else:
            messages.error(request, "An error has occured during registration.")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)
