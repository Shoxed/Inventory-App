from django.db import models

# Create your models here.

class Item(models.Model):
    CATEGORY = [
        ("Dairy", "Dairy"),
        ("Protein", "Protein"),
        ("Bread", "Bread"),
        ("Fruit", "Fruit"),
        ("Vegetable", "Vegetable"),
        ("Beverage", "Beverage"),
        ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=CATEGORY)
    cost = models.FloatField()
    amount = models.IntegerField()

