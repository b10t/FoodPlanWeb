"""FoodPlan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from planes.views import (
    index,
    order,
    personal_account,
    SignUpView,
    make_payment,
    successful_payment
)
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lk/', personal_account, name='personal_account'),
    path(
        'login/',
        LoginView.as_view(template_name='auth.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='lk.html'),
        name='logout'
    ),
    path('order/', order, name='order'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('', index, name='index'),
    path('make_payment/<str:payment_id>/', make_payment, name='make_payment'),
    path(
        'successful_payment/<str:payment_id>/',
        successful_payment,
        name='successful_payment'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
