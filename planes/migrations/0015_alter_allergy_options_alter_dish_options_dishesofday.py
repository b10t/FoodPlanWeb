# Generated by Django 4.1.2 on 2022-10-10 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0014_alter_allergy_options_alter_dish_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allergy',
            options={'ordering': ['sort_order'], 'verbose_name': 'Аллергия', 'verbose_name_plural': 'Аллергии'},
        ),
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name': 'Блюдо', 'verbose_name_plural': 'Блюда'},
        ),
        migrations.CreateModel(
            name='DishesOfDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата добавления записи')),
                ('dishes_of_day', models.TextField(verbose_name='Блюда_дня')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Блюда_дня',
                'verbose_name_plural': 'Блюда_дней',
            },
        ),
    ]