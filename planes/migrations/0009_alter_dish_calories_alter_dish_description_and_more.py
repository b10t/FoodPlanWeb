# Generated by Django 4.1.2 on 2022-10-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0008_menutype_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='calories',
            field=models.IntegerField(default='', verbose_name='Калорийность'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='recipe',
            field=models.TextField(blank=True, verbose_name='Рецепт приготовления'),
        ),
    ]
