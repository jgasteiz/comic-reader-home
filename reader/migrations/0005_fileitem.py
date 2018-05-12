# Generated by Django 2.0 on 2018-05-12 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0004_auto_20180124_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=512)),
                ('path', models.TextField(blank=True)),
                ('file_type', models.CharField(blank=True, choices=[('comic', 'comic'), ('directory', 'directory')], max_length=12)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='reader.FileItem')),
            ],
            options={
                'ordering': ['-file_type', 'name'],
            },
        ),
    ]