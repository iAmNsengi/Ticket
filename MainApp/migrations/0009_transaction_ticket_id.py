# Generated by Django 4.2.2 on 2023-07-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0008_alter_transaction_options_transaction_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='ticket_id',
            field=models.CharField(default='0', max_length=20),
        ),
    ]
