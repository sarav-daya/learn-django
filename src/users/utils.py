from django.db.models import Q
from users.models import Profile, Skill
from django.core.paginator import Paginator


def search_projects(request):

    search = ""

    if request.GET.get("search"):
        search = request.GET.get("search")

    # profiles = Profile.objects.filter(name__icontains=search, short_intro__icontains=search)
    # profiles = Profile.objects.filter(Q(name__icontains=search) | Q(short_intro__icontains=search))

    # skills = Skill.objects.filter(name__iexact=search)
    skills = Skill.objects.filter(name__icontains=search)

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search)
        | Q(short_intro__icontains=search)
        | Q(skill__in=skills)
    )

    return search, profiles
