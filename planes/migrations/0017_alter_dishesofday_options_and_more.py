# Generated by Django 4.1.2 on 2022-10-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0016_dishesofday_menu_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dishesofday',
            options={'verbose_name': 'Блюда дня', 'verbose_name_plural': 'Блюда дней'},
        ),
        migrations.AlterField(
            model_name='dishesofday',
            name='dishes_of_day',
            field=models.TextField(verbose_name='Блюда дня'),
        ),
    ]
