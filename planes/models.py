import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]


class MenuType(models.Model):
    name = models.CharField(
        unique=True,
        max_length=255,
        blank=False,
        default='',
        verbose_name='Наименование меню',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    image = models.ImageField(
        blank=True,
        verbose_name='Картинка'
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
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    recipe = models.TextField(
        blank=True,
        verbose_name='Рецепт приготовления',
    )
    calories = models.PositiveIntegerField(
        default=0,
        blank=False,
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


class DishIngredient(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
        related_name='ingredients_dish'
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


class UTM(models.Model):
    source = models.CharField('источник перехода', max_length=100)
    medium = models.CharField('тип трафика', max_length=100)
    campaign = models.CharField('название компании', max_length=100)
    content = models.CharField(
        'информация о содержимом',
        max_length=100,
        default=None,
        null=True
    )
    term = models.CharField(
        'ключевое слово',
        max_length=100,
        default=None,
        null=True
    )
    created_at = models.DateTimeField(
        'дата создания',
        auto_now_add=True,
        editable=False
    )

    def __str__(self):
        return f"{self.source} {self.campaign}"


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='subscribes'
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
    calories = models.PositiveIntegerField(
        default=0,
        blank=False,
        verbose_name='Калории',
    )
    payment_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        verbose_name='Идентификатор платежа'
    )
    stripe_payment_id = models.CharField(
        max_length=100,
        blank=True,
        default='',
        editable=False,
        verbose_name='Ид. платежа stripe'
    )
    cost = models.IntegerField(
        'стоимость месяца подписки в рублях',
        default=100
    )
    subscription_paid = models.BooleanField(
        blank=False,
        default=False,
        verbose_name='Подписка оплачена'
    )
    utm = models.ForeignKey(
        UTM,
        on_delete=models.PROTECT,
        verbose_name='UTM-метка',
        related_name='subscribes',
        default=None,
        null=True
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписка'

    def __str__(self):
        return f'Подписка "{self.id}"'
