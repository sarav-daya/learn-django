from django.shortcuts import render


def frontend(request):
    context = {}
    return render(request, "frontend.html", context)
