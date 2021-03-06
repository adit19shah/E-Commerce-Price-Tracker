# Generated by Django 3.1.4 on 2020-12-28 06:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amazon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('URL', models.CharField(max_length=200)),
                ('Desired_price', models.FloatField()),
                ('Email', models.EmailField(max_length=254)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 12, 28, 12, 21, 35, 124926))),
            ],
        ),
        migrations.CreateModel(
            name='Ebay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('URL', models.CharField(max_length=200)),
                ('Desired_price', models.FloatField()),
                ('Email', models.EmailField(max_length=254)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 12, 28, 12, 21, 35, 125943))),
            ],
        ),
        migrations.CreateModel(
            name='Flipkart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('URL', models.CharField(max_length=200)),
                ('Desired_price', models.FloatField()),
                ('Email', models.EmailField(max_length=254)),
                ('time', models.DateTimeField(default=datetime.datetime(2020, 12, 28, 12, 21, 35, 123944))),
            ],
        ),
    ]
