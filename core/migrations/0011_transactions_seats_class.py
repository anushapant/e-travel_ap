# Generated by Django 2.2.13 on 2020-11-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20201119_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='seats_class',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
