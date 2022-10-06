import os
import json
from unicodedata import name
from django.core.management.base import BaseCommand
from planes.models import *


def load_menu_dishes(menu_type, dishes_json):
    menu = MenuType(name=menu_type)
    menu.save()
    with open(dishes_json, 'r', encoding='utf-8')as file:
        dishes = json.load(file)
    for dish in dishes[:25]:
        print(f"Dish: {dish['title']}, {dish['calories']}")
        new_dish = Dish(
            menu_type=menu,
            name=dish['title'][:255],
            description=dish['description'][:2048],
            recipe=dish['recept'][:2048],
            calories=dish['calories'],
            picture=dish['img_url']
        )
        new_dish.save()
        for ingredient in dish['ingredients']:
            DishIngredient(
                dish=new_dish,
                name=ingredient['name'],
                amount=ingredient['amount'],
                unit=ingredient['measurement']
            ).save()

    print(f' Загружено блюд для меню "{menu_type}" '
          f'{Dish.objects.filter(menu_type=menu).count()}')


class Command(BaseCommand):
    help = 'Loads disheses'

    def handle(self, *args, **options):
        try:
            load_menu_dishes(menu_type='Классическое', dishes_json='json/classic_dishes.json')
            load_menu_dishes(menu_type='Низкоуглеводное', dishes_json='json/low_card_dishes.json')
            load_menu_dishes(menu_type='Кето', dishes_json='json/keto_dish.json')
            load_menu_dishes(menu_type='Вегетарианское', dishes_json='json/vegan_dishes.json',)
        except json.decoder.JSONDecodeError:
            print('Что-то пошло не так! Проверте ссылку и повторите.')
        except TypeError:
            print('Что-то пошло не так! Проверте ссылку и повторите.')
