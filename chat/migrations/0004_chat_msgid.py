# Generated by Django 4.0.7 on 2023-03-07 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chat_original_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='msgID',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
