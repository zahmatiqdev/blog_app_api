# Generated by Django 3.2.11 on 2022-02-16 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220210_0513'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]