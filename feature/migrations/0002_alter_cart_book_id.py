# Generated by Django 4.1.7 on 2023-03-09 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0004_rename_genre_name_genre_name"),
        ("feature", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="book_id",
            field=models.ManyToManyField(blank=True, to="product.book"),
        ),
    ]
