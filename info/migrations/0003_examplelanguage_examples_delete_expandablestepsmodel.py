# Generated by Django 4.0.7 on 2023-03-05 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_expandablestepsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('language', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Examples',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('body', models.TextField(blank=True)),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='info.examplelanguage')),
            ],
        ),
        migrations.DeleteModel(
            name='ExpandableStepsModel',
        ),
    ]