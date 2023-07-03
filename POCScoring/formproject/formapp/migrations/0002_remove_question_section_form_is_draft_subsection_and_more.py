# Generated by Django 4.2.2 on 2023-06-30 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='section',
        ),
        migrations.AddField(
            model_name='form',
            name='is_draft',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('order', models.IntegerField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formapp.section')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='subsection',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='formapp.subsection'),
            preserve_default=False,
        ),
    ]