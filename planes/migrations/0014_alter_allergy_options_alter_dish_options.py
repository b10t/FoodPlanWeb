# Generated by Django 4.1.2 on 2022-10-10 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0013_alter_dishingredient_allergy_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allergy',
            options={'verbose_name': 'Блюдо', 'verbose_name_plural': 'Блюда'},
        ),
        migrations.AlterModelOptions(
            name='dish',
            options={},
        ),
    ]
