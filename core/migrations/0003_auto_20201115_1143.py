# Generated by Django 2.2.13 on 2020-11-15 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201115_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightticket',
            name='seat_no',
        ),
        migrations.AddField(
            model_name='flightticket',
            name='number_seats',
            field=models.IntegerField(default=26),
        ),
        migrations.AddField(
            model_name='flightticket',
            name='number_seats_available',
            field=models.IntegerField(default=26),
        ),
    ]
