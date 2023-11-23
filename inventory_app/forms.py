from django.forms import ModelForm
from .models import Item, Employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


#create class for item form
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'category', 'cost', 'amount' )

class EmployeeForm(ModelForm):
    class Meta: 
        model = Employee
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']