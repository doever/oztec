# Generated by Django 2.0.6 on 2018-08-08 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminte', '0003_auto_20180808_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='is_del',
            field=models.BooleanField(default=0),
        ),
    ]