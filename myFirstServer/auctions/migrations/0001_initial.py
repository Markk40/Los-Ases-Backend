# Generated by Django 5.1.7 on 2025-03-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Auction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "discount_percentage",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("rating", models.DecimalField(decimal_places=2, max_digits=3)),
                ("stock", models.IntegerField()),
                ("brand", models.CharField(max_length=100)),
                ("category", models.CharField(max_length=50)),
                ("thumbnail", models.URLField()),
            ],
        ),
    ]
