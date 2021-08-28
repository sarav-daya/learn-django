from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q


from users.models import Profile, Skill
from users.utils import search_projects


from users.forms import CustomUserCreationForm, MessageForm, ProfileForm, SkillForm

# Create your views here.
def profiles(request):

    search, profiles = search_projects(request)

    context = {"profiles": profiles, "search": search}
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
        "projects": projects,
    }
    return render(request, "users/account.html", context)


def login_page(request):
    print(request.GET.get("next"))
    if request.user.is_authenticated:
        return redirect("profiles")

    context = {}

    if request.method == "POST":

        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Invalid username or password")
            return render(request, "users/login_register.html", context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")
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
            return redirect("edit-account")
        else:
            messages.error(request, "An error has occured during registration.")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def create_skill(request):
    form = SkillForm()
    profile = request.user.profile
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="login")
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        return redirect("account")

    context = {"object": skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    msg = profile.messages.all()
    unread_count = msg.filter(is_read=False).count()
    context = {"msg": msg, "unread_count": unread_count}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def messagebox(request, pk):
    profile = request.user.profile
    msg = profile.messages.get(id=pk)
    if msg.is_read == False:
        msg.is_read = True
        msg.save()
    context = {
        "message": msg,
    }

    return render(request, "users/message.html", context)


def create_message(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)
