# Generated by Django 4.2.2 on 2023-07-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0010_remove_formassignment_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='formassignment',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
