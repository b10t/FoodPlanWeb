import stripe
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.edit import CreateView

from planes.forms import CustomUserChangeForm, CustomUserCreationForm
from planes.models import Allergy, MenuType, Subscribe


def redirect_payment_url(request):
    meals_number = 4 - int(request.GET.get('select1')) \
        - int(request.GET.get('select2')) \
        - int(request.GET.get('select3')) \
        - int(request.GET.get('select4'))
    subscription = Subscribe()
    subscription.user = request.user
    duration = int(request.GET.get('duration'))
    if duration == 0:
        subscription.duration = 1
    if duration == 1:
        subscription.duration = 3
    if duration == 2:
        subscription.duration = 6
    if duration == 3:
        subscription.duration = 12
    subscription.number_of_meals = meals_number
    subscription.number_of_person = int(
        request.GET.get('persons_number')
    ) + 1
    menu_type = request.GET.get('foodtype')
    if menu_type == 'classic':
        subscription.menu_type = MenuType.objects.get(name='Классическое')
    if menu_type == 'low':
        subscription.menu_type = MenuType.objects.get(
            name='Низкоуглеводное'
        )
    if menu_type == 'veg':
        subscription.menu_type = MenuType.objects.get(
            name='Вегетарианское'
        )
    if menu_type == 'keto':
        subscription.menu_type = MenuType.objects.get(name='Кето')
    calories = request.GET.get('calories')
    if calories:
        subscription.calories = int(calories)
    subscription.save()
    allergy_ids = list()
    for key, value in request.GET.items():
        if key.startswith('allergy'):
                allergy_ids.append(int(value))
    for allergy_id in allergy_ids:
        subscription.allergy.add(Allergy.objects.get(id=allergy_id))
    payment_url = request.build_absolute_uri(
        reverse(
            'make_payment',
            kwargs={'payment_id': subscription.payment_id}
        )
    )
    return redirect(payment_url, code=303)


class SignUpView(CreateView):

    template_name = 'registration.html'
    def get(self, request):
        form = CustomUserCreationForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('personal_account')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        result = super().form_valid(form)
        new_user = authenticate(
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, new_user)
        return result


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
    elif request.method == 'GET' and 'order' in request.session:
        request.GET = request.session['order']
        del request.session['order']

        return redirect_payment_url(request)
    else:
        form = CustomUserChangeForm()

    django_messages = messages.get_messages(request)
    if django_messages:
        for message in django_messages:
            message = message
    context = {
        'form': form,
        'message': message,
        'subscribes': user.subscribes.all()
    }

    return render(request, 'lk.html', context)


def order(request):
    context = {'allergies': Allergy.objects.all()}

    if 'foodtype' in request.GET and request.user.is_authenticated:
        redirect_payment_url(request)
    if 'foodtype' in request.GET and not request.user.is_authenticated:
        request.session['order'] = request.GET
        return redirect('login')
    return render(request, 'order.html', context)


def make_payment(request, payment_id):
    """Make payment."""
    stripe.api_key = settings.STRIPE_API_KEY

    try:
        subscription = Subscribe.objects.get(payment_id=payment_id)
    except ValidationError:
        return HttpResponseNotFound('Неверный формат id платежа.')
    except Subscribe.DoesNotExist:
        return HttpResponseNotFound(f'Платёж {payment_id} не найден.')

    if subscription.subscription_paid:
        return HttpResponseNotFound(f'Платёж {payment_id} оплачен.')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Ваш заказ №{subscription.payment_id}',
                },
                'unit_amount': subscription.cost * 100,
            },
            'quantity': subscription.duration,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('successful_payment', kwargs={'payment_id': payment_id})),
        cancel_url=request.build_absolute_uri(reverse('order')),
        client_reference_id=payment_id,
        customer_email=request.user.email,
    )

    subscription.stripe_payment_id = session.id
    subscription.save()

    return redirect(session.url, code=303)


def successful_payment(request, payment_id):
    try:
        subscription = Subscribe.objects.get(payment_id=payment_id)
    except ValidationError:
        return HttpResponseNotFound('Неверный формат id платежа.')
    except Subscribe.DoesNotExist:
        return HttpResponseNotFound(f'Платёж {payment_id} не найден.')

    subscription.subscription_paid = True
    subscription.save()
    messages.success(request, 'Подписка успешно оплачена.')

    return redirect('personal_account')
