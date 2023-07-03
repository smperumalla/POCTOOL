# Generated by Django 4.2.2 on 2023-07-03 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0011_formassignment_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='subsection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='formapp.subsection'),
        ),
        migrations.AlterField(
            model_name='section',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formapp.form'),
        ),
        migrations.AlterField(
            model_name='subsection',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formapp.section'),
        ),
    ]
