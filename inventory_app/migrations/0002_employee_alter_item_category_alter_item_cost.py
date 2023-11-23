# Generated by Django 4.2.7 on 2023-11-22 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('emply_id', models.IntegerField()),
                ('position', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Dairy', 'Dairy'), ('Protein', 'Protein'), ('Bread', 'Bread'), ('Fruit', 'Fruit'), ('Vegetable', 'Vegetable'), ('Beverage', 'Beverage')], max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='cost',
            field=models.FloatField(blank=True),
        ),
    ]