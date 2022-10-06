import random

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Должна быть электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(verbose_name='имя', max_length=150)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)
    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    def __str__(self):
        return f'{self.username}, {self.email if self.email else "no email"}'

    def get_full_name(self):
        return f'{self.username}, {self.email if self.email else "no email"}'

    def get_short_name(self):
        return self.username


class MenuType(models.Model):
    name = models.CharField(
        max_length=255, unique=True, blank=False, default='',
        verbose_name='Наименование меню',
    )

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = 'Типы меню'

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(
        max_length=255, unique=True, blank=False, default='',
        verbose_name='Наименование аллергии',
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    class Meta:
        verbose_name = 'Аллергия'
        verbose_name_plural = 'Аллергии'
        ordering = ['sort_order']

    def __str__(self):
        return self.name


class Dish(models.Model):
    menu_type = models.ForeignKey(
        MenuType,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Тип меню',
        related_name='dish_menu_type'
    )
    name = models.CharField(
        max_length=255, blank=False, default='',
        verbose_name='Наименование',
    )
    description = models.CharField(
        max_length=2048, blank=True,
        verbose_name='Описание',
    )
    recipe = models.CharField(
        max_length=2048, blank=True,
        verbose_name='Рецепт приготовления',
    )
    calories = models.CharField(
        max_length=20, blank=False,
        default='',
        verbose_name='Калорийность',
    )
    picture = models.URLField(
        max_length=4096,
        verbose_name='Ссылка на картинку',
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return f'Блюдо "{self.name}"'

    def get_allergies(self):
        dish_allergy = []
        for dish_ingredient in self.ingredient_dish.all():
            dish_allergy = set(dish_allergy) | \
                set(dish_ingredient.allergy.filter(~Q(name="нет")))
        return dish_allergy

    def get_full_description(self):
        dish_description = f'''{self.picture}
Блюдо: {self.name}
Описание: {self.description}
Рецепт приготовления: {self.recipe}
Калорийность: {self.calories}
Ингредиенты:
'''
        for ingredient in self.ingredient_dish.all():
            dish_description += f'{ingredient.name}, {ingredient.amount}, ' \
                                f'{ingredient.unit}\n'
        return dish_description


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
        related_name='ingredient_dish'
    )
    name = models.CharField(
        max_length=255, blank=False, default='',
        verbose_name='Ингредиент'
    )
    amount = models.CharField(
        max_length=20, default='',
        verbose_name='Количество'
    )
    unit = models.CharField(
        max_length=255, blank=False, default='',
        verbose_name='Единица измерения'
    )
    allergy = models.ManyToManyField(
        Allergy,
        related_name='ingredient_allergy',
    )

    class Meta:
        verbose_name = 'Ингредиент блюда'
        verbose_name_plural = 'Ингредиенты блюд'

    def __str__(self):
        return f'Блюдо "{self.name}"'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='subscribe_user'
    )
    number_of_meals = models.IntegerField(
        blank=False, default=1,
        verbose_name='Количество приёмов пищи за день',
    )
    number_of_person = models.IntegerField(
        blank=False, default=1,
        verbose_name='Количество персон',
    )
    allergy = models.ManyToManyField(
        Allergy,
        verbose_name='Аллергии',
        # related_name='subscribe_allergies'
    )
    menu_type = models.ForeignKey(
        MenuType,
        on_delete=models.DO_NOTHING,
        verbose_name='Тип меню',
        related_name='subscribe_menu_type'
    )
    duration = models.IntegerField(
        default=1,
        verbose_name='Длительность подписки, мес.',
    )
    subscription_paid = models.BooleanField(
        blank=False,
        default=False,
        verbose_name='Подписка оплачена'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f'Подписка "{self.id}"'

    def get_allergies(self):
        allergies = ''
        for allergy in self.allergy.all():
            allergies += f'{str(allergy)}, '
        return allergies[:-2]

    def get_subscribe_dish(self):
        subs_allergies = set(self.allergy.filter(~Q(name="нет")))
        dishes = []
        for dish in Dish.objects.filter(menu_type=self.menu_type):
            if not dish.get_allergies() & subs_allergies:
                dishes.append(dish)
        return dishes[random.randint(0, len(dishes) - 1)].get_full_description()

    def get_subscribe_description(self):
        return f'Пользователь: {self.user}\n' \
               f'Количество приёмов пищи за день: {self.number_of_meals}\n' \
               f'Количество персон: {self.number_of_person}\n' \
               f'Аллергии: {self.get_allergies()}\n' \
               f'Тип меню: {self.menu_type}\n' \
               f'Длительность подписки, мес.: {self.duration}\n' \
               f'Подписка оплачена: {"да" if self.subscription_paid else "нет"}'
