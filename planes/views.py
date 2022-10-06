from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration.html'


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
