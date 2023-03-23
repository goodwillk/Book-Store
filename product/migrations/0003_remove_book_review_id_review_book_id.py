# Generated by Django 4.1.7 on 2023-03-06 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_alter_review_rating"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="review_id",
        ),
        migrations.AddField(
            model_name="review",
            name="book_id",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review_to_book",
                to="product.book",
            ),
        ),
    ]