# Generated by Django 5.0.1 on 2024-02-18 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_delete_requirements'),
    ]

    operations = [
        migrations.CreateModel(
            name='lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.course')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(null=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='Media/Miniature')),
                ('youtube_id', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=100)),
                ('time_duration', models.FloatField(null=True)),
                ('preview', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.lesson')),
            ],
        ),
    ]