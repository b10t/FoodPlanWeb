from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

import stripe
from planes.models import Subscribe, Allergy, MenuType
from planes.forms import CustomUserCreationForm


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
    print(f'request: {request}')
    print(f'GET: {request.GET}')
    print(f'POST: {request.POST}')
    context = {'allergies': Allergy.objects.all()}
    if 'foodtype' in request.GET:
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
    context = {}

    try:
        subscription = Subscribe.objects.get(payment_id=payment_id)
    except ValidationError:
        return HttpResponseNotFound('Неверный формат id платежа.')
    except Subscribe.DoesNotExist:
        return HttpResponseNotFound(f'Платёж {payment_id} не найден.')

    subscription.subscription_paid = True
    subscription.save()

    return render(request, 'lk.html', context)
