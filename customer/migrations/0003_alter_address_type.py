# Generated by Django 4.1.7 on 2023-03-06 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0002_rename_address_type_address_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="type",
            field=models.CharField(
                choices=[("Work Address", "Work"), ("Home Address", "Home")],
                max_length=150,
            ),
        ),
    ]