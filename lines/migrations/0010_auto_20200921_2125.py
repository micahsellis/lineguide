# Generated by Django 3.1.1 on 2020-09-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lines', '0009_auto_20200921_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='postal_code',
            field=models.CharField(max_length=10),
        ),
    ]
