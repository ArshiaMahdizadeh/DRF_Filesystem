# Generated by Django 5.0.4 on 2024-04-16 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_fileupload_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_size', models.BigIntegerField()),
                ('file_type', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='main.fileupload')),
            ],
        ),
    ]
