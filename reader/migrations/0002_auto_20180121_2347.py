# Generated by Django 2.0 on 2018-01-21 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='page',
        ),
        migrations.AddField(
            model_name='bookmark',
            name='page_num',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='title',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]