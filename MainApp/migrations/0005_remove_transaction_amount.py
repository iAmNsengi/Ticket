# Generated by Django 4.2.2 on 2023-07-25 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_alter_transaction_departure_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='amount',
        ),
    ]
