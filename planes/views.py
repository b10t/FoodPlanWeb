from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    context = {
    }

    return render(request, 'index.html', context)
