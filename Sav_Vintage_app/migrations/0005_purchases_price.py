# Generated by Django 5.1.6 on 2025-03-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sav_Vintage_app', '0004_cars_is_available_purchases'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='price',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
