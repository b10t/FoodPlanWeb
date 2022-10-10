import json

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.http import JsonResponse
from django.urls import path

from planes.forms import CustomUserCreationForm
from planes.models import (
    DishesOfDay,
    MenuType,
    Allergy,
    Dish,
    DishIngredient,
    Subscribe,
    UTM
)

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ("username", 'email', 'password1', 'password2'),
            },
        ),
    )
    add_form = CustomUserCreationForm


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ['sort_order', 'name']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['menu_type', 'name', 'recipe']
    list_filter = ['menu_type']


@admin.register(DishIngredient)
class DishIngredientAdmin(admin.ModelAdmin):
    list_display = ['dish_id', 'id', 'dish', 'name', 'amount', 'unit']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['id', 'number_of_meals', 'number_of_person', 'menu_type',
                    'duration']


@admin.register(DishesOfDay)
class DishesOfDay(admin.ModelAdmin):


@admin.register(UTM)
class UTMAdmin(admin.ModelAdmin):
    list_display = [
        'source',
        'medium',
        'campaign',
        'content',
        'term',
        'created_at'
    ]

    def changelist_view(self, request, extra_context=None):
        chart_data = self.chart_data()
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        print(f'chart_data: {as_json}')
        extra_context = extra_context or {'chart_data': as_json}

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path('chart_data/', self.admin_site.admin_view(self.chart_data_endpoint)),
        ]
        return extra_urls + urls

    def chart_data_endpoint(self, request):
        chart_data = self.chart_data()
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self):
        return UTM.objects.values('source').annotate(y=Count('source'))
