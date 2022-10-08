from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from planes.forms import CustomUserCreationForm
from planes.models import (
    MenuType,
    Allergy,
    Dish,
    DishIngredient,
    Subscribe
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
class Subscribe(admin.ModelAdmin):
    list_display = ['id', 'number_of_meals', 'number_of_person', 'menu_type',
                    'duration']
