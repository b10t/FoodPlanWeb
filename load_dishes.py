import json
from planes.models import Dish, MenuType, DishIngredient


def load_menu_dishes(dishes_json, menu_type):
    try:
        menu = MenuType.objects.get(name=menu_type)
    except Exception as e:
        print(f'Ошибка для "{menu_type}"! {e}')
        return

    print(f' Удаление блюд меню "{menu_type}" перед загрузкой...')
    try:
        Dish.objects.filter(menu_type=menu).delete()
        print(f' Удаление завершено')
    except Exception as e:
        print(f'Ошибка удаления блюд: {e}')
        return

    with open(dishes_json, 'r', encoding='utf-8') as f:
        dishes = json.load(f)

    for dish in dishes[:25]:
        print(f"Dish: {dish['title']}, {dish['calories']}")
        new_dish = Dish(
            menu_type=menu,
            name=dish['title'][:255],
            description=dish['description'][:2048],
            recipe=dish['recept'][:2048],
            calories=dish['calories'][:20],
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


def load_all_dishes():
    load_menu_dishes('json/classic_dishes.json', 'Классическое')
    load_menu_dishes('json/low_card_dishes.json', 'Низкоуглеводное')
    load_menu_dishes('json/keto_dish.json', 'Кето')
    load_menu_dishes('json/vegan_dishes.json', 'Вегетарианское')


if __name__ == '__main__':
    load_all_dishes()
