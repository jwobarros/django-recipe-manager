# Generated by Django 4.2 on 2023-04-26 23:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0003_alter_ingredient_measurement_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
