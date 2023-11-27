from django.forms import ModelForm
from .models import Item, Employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# form for creating, updating, and deleting item model
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'category', 'cost', 'amount' )

# form for creating and updating employee model
class EmployeeForm(ModelForm):
    class Meta: 
        model = Employee
        fields = '__all__'
        exclude = ['user']

# form for creatting a user 
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']