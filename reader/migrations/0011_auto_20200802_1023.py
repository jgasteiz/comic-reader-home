# Generated by Django 3.0.8 on 2020-08-02 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reader", "0010_fileitem_furthest_read_page"),
    ]

    operations = [
        migrations.RemoveField(model_name="bookmark", name="comic",),
        migrations.DeleteModel(name="Favorite",),
        migrations.DeleteModel(name="Bookmark",),
    ]
