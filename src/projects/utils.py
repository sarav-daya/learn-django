from projects.models import Tag, Project
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_projects(request):
    # search = ""
    # page = 1
    # if request.GET.get("search"):
    #     search = request.GET.get("search")

    # if request.GET.get("page"):
    #     try:
    #         page = int(request.GET.get("page"))
    #     except:
    #         page = 1

    # tags = Tag.objects.filter(name__icontains=search)

    # projects = (
    #     Project.objects.distinct().filter(
    #         Q(title__icontains=search)
    #         | Q(description__icontains=search)
    #         | Q(owner__name__icontains=search)
    #         | Q(tags__in=tags)
    #     )
    #     # .order_by("created") We can order it by this way or the other way is to define ordering = ["created"]
    #     # in meta class to reverse the order we need to add a minus symbol like ordering = ["-created"]
    # )

    # p = Paginator(projects, 3)
    # if page > p.num_pages:
    #     page = p.num_pages

    # return search, p.page(page)
    search = ""
        
    if request.GET.get("search"):
        search = request.GET.get("search")    

    tags = Tag.objects.filter(name__icontains=search)

    projects = (
        Project.objects.distinct().filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(owner__name__icontains=search)
            | Q(tags__in=tags)
        )
        # .order_by("created") We can order it by this way or the other way is to define ordering = ["created"]
        # in meta class to reverse the order we need to add a minus symbol like ordering = ["-created"]
    )
    return search, projects