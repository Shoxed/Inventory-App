from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import *


# Inventory Item Views 
class ItemListView(generic.ListView):
    model = Item

class ItemDetailView(generic.DetailView):
    model = Item


def index(request):
# Render index.html
    return render( request, 'inventory_app/index.html')

