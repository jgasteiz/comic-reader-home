# Generated by Django 2.0 on 2019-02-19 18:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("reader", "0006_auto_20180516_1831")]

    operations = [
        migrations.AlterField(
            model_name="fileitem",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="reader.FileItem",
            ),
        )
    ]