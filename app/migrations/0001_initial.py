# Generated by Django 5.1.1 on 2024-10-06 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CropSalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_sales', models.PositiveIntegerField(default=0)),
                ('highest_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.crop')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.district')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_sold', models.PositiveIntegerField()),
                ('price_per_kg', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('crop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.crop')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.district')),
            ],
        ),
    ]
