from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    context = {
    }

    return render(request, 'index.html', context)


@login_required
def personal_account(request):
    context = {
    }

    return render(request, 'lk.html', context)


@login_required
def order(request):
    context = {
    }

    return render(request, 'order.html', context)


def registration(request):
    context = {
    }

    return render(request, 'registration.html', context)
