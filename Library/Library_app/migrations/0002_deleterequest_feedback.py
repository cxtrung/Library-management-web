# Generated by Django 4.0.3 on 2023-11-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Library_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_request', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
