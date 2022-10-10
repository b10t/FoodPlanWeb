# Generated by Django 4.1.2 on 2022-10-09 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0012_alter_dishingredient_dish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishingredient',
            name='allergy',
            field=models.ManyToManyField(related_name='allergy_ingredients', to='planes.allergy'),
        ),
        migrations.AlterField(
            model_name='dishingredient',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dish_ingredients', to='planes.dish', verbose_name='Блюдо'),
        ),
    ]
