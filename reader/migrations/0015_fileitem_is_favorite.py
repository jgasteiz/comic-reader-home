# Generated by Django 3.2.5 on 2022-04-03 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reader", "0014_alter_fileitem_file_type_alter_fileitem_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileitem",
            name="is_favorite",
            field=models.BooleanField(default=False),
        ),
    ]
