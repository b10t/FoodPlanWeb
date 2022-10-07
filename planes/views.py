from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserChangeForm, CustomUserCreationForm


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
    user = request.user
    message = ''

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)

        # Костыль из-за disabled в input
        form.errors.pop('email', None)

        form_data = form.data.copy()
        form_data['email'] = user.email

        form.data = form_data

        if form.is_valid():
            user = form.save()

            message = 'Данные успешно изменены.'

            if password := form.cleaned_data.get('password1'):
                user.set_password(password)
                user.save()

                update_session_auth_hash(request, user)

                message = 'Пароль успешно изменён.'

    else:
        form = CustomUserChangeForm()

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'lk.html', context)


@login_required
def order(request):
    context = {
    }

    return render(request, 'order.html', context)
