# Generated by Django 4.2.2 on 2023-06-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, verbose_name='Phone Number')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='Registered at')),
                ('last_login_at', models.DateTimeField(editable=False, verbose_name='Last Login at')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ('last_name', 'first_name'),
            },
        ),
    ]