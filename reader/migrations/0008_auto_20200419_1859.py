# Generated by Django 2.2.10 on 2020-04-19 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reader", "0007_auto_20190219_1818"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bookmark", old_name="page_num", new_name="page_number",
        ),
    ]
