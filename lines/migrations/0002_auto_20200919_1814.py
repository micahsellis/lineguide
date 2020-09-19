# Generated by Django 3.1.1 on 2020-09-19 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lines', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='line',
            old_name='food_type',
            new_name='category',
        ),
        migrations.AddField(
            model_name='line',
            name='line_type',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
