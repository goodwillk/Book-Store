# Generated by Django 4.1.7 on 2023-03-06 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="address_type",
            new_name="type",
        ),
    ]