# Generated by Django 4.1.5 on 2023-03-14 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0010_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]