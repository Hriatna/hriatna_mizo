# Generated by Django 4.0.7 on 2023-02-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_translated_query'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='original_response',
            field=models.TextField(blank=True),
        ),
    ]
