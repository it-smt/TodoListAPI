# Generated by Django 4.2.9 on 2024-02-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('D', 'Готово'), ('N', 'Не готово')], default='N', max_length=1),
        ),
    ]