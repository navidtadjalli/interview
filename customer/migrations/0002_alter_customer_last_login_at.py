# Generated by Django 4.2.2 on 2023-06-22 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='last_login_at',
            field=models.DateTimeField(editable=False, null=True, verbose_name='Last Login at'),
        ),
    ]
