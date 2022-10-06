from django.contrib import admin

from planes.models import (
    User,
    MenuType,
    Allergy,
    Dish,
    DishIngredient,
    Subscribe
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'email',
        'username',
        'is_staff',
        'is_active',
        'is_admin',
    ]
    search_fields = ('username', 'email')

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
