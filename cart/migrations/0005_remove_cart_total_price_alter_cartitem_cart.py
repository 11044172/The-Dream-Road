# Generated by Django 4.2.14 on 2024-08-15 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0004_cart_total_price"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="total_price",
        ),
        migrations.AlterField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cartitem_set",
                to="cart.cart",
            ),
        ),
    ]
