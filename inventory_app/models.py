from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

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
    cost = models.FloatField(blank=True)
    amount = models.IntegerField()
    
    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])


class Employee(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('user_page', args=[str(self.user_id)])