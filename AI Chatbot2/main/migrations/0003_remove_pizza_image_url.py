# Generated by Django 5.1.6 on 2025-03-01 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_beverage_order_pizza_size_delete_chatmessage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='image_url',
        ),
    ]
