# Generated by Django 4.2.14 on 2024-08-13 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "registration",
            "0003_user_groups_user_is_superuser_user_user_permissions_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="メールアドレス"
            ),
        ),
    ]
