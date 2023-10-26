# Generated by Django 4.2.6 on 2023-10-26 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Dairy', 'Dairy Product'), ('Protein', 'Protein Product')], max_length=200)),
                ('cost', models.FloatField()),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
