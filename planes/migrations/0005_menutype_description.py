# Generated by Django 4.1.2 on 2022-10-07 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planes', '0004_auto_20221006_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='menutype',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
