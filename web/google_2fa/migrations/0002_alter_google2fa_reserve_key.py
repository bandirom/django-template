# Generated by Django 3.2.11 on 2022-04-27 14:55

from django.db import migrations, models
import google_2fa.models


class Migration(migrations.Migration):

    dependencies = [
        ('google_2fa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='google2fa',
            name='reserve_key',
            field=models.CharField(default=google_2fa.models.generate_reserve_key, max_length=200),
        ),
    ]
