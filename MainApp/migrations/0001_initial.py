# Generated by Django 4.2.2 on 2023-07-21 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From', models.CharField(max_length=30)),
                ('To', models.CharField(max_length=30)),
                ('price', models.FloatField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.agency')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('passcode', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.CharField(max_length=100)),
                ('departure_time', models.DateTimeField()),
                ('no_tickets', models.IntegerField()),
                ('amount', models.FloatField()),
                ('date', models.DateField(null=True)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.destination')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.userprofile')),
            ],
        ),
    ]
