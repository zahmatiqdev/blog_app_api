# Generated by Django 3.2.12 on 2022-03-09 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_user_is_editor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='author',
            new_name='user',
        ),
    ]