from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect
from projects.models import Project
from projects.forms import ProjectForm, ReviewForm

from projects.utils import search_projects

NO_OF_RESULT_PER_PAGE = 6


def projects(request):
    search, projects = search_projects(request)
    page = request.GET.get("page")
    paginator = Paginator(projects, NO_OF_RESULT_PER_PAGE)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    context = {"projects": projects, "search": search, "paginator": paginator}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    project = Project.objects.get(id=pk)

    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.get_vote_count

        return redirect("project", pk=project.id)

    tags = project.tags.all()
    return render(
        request,
        "projects/single-project.html",
        {
            "project": project,
            "tags": tags,
            "form": form,
        },
    )


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        return redirect("account")

    context = {"object": project}
    return render(request, "delete_template.html", context)
