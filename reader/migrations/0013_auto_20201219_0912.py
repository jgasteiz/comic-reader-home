# Generated by Django 3.0.8 on 2020-12-19 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0012_fileitem_is_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fileitem',
            options={'ordering': ['name']},
        ),
    ]