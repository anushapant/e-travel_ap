# Generated by Django 2.2.13 on 2020-11-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_flight_booking_list_additional'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightticket',
            name='destination_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='flightticket',
            name='start_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
