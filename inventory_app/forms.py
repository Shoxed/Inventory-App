from django.forms import ModelForm
from .models import Item


#create class for project form
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'category', 'cost', 'amount' )