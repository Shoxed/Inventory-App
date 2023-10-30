from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import *
from .forms import ItemForm


# Inventory Item Views 
class ItemListView(generic.ListView):
    model = Item

class ItemDetailView(generic.DetailView):
    model = Item

def addItem(request):
    form = ItemForm()

    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        item_data = request.POST.copy()
        
        form = ItemForm(item_data)
        if form.is_valid():
            # Save the form without committing to the database
            item = form.save(commit=False)
            # Set the portfolio relationship
            item.save()

            # Redirect back to the inventory page
            return redirect('inventory')

    # Render the form template if the request method is GET
    context = {'form': form}
    return render(request, 'inventory_app/item_form.html', context)


def deleteItem(request, pk):
    item = Item.objects.get(pk=pk)

    if request.method == 'POST':
        item.delete() 
        return redirect('inventory')
    
    context = {'item': item}
    return render(request, 'inventory_app/item_delete.html', context)


def updateItem(request, pk):
    item = Item.objects.get(pk=pk)
    form = ItemForm(instance=item)
  
    if request.method == 'POST':
        form = ItemForm(request.POST, instance = item)

        if form.is_valid():
            form.save()
            return redirect('inventory')

    context={'form': form, 'item': item}
    return render(request, 'inventory_app/item_update.html', context)


def index(request):
# Render index.html
    return render( request, 'inventory_app/index.html')

