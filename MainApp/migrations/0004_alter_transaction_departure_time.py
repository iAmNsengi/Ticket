# Generated by Django 4.2.2 on 2023-07-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_remove_transaction_no_tickets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='departure_time',
            field=models.TimeField(),
        ),
    ]