# Generated by Django 5.0.4 on 2024-04-17 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_fileupload_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
    ]