# Generated by Django 2.2.13 on 2020-11-15 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201115_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='flightticket',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
