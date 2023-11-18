from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import *
from .forms import ItemForm, CreateUserForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required(login_url='login')
@allowed_users(allowed_roles='employee')
def userPage(request):
    employee = request.user.employee
    form = EmployeeForm(instance = employee)
    print('employee', employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance = employee)
        if form.is_valid():
            form.save
    
    context = {'form': form}
    return render(request, 'inventory_app/user.html', context)


# Inventory Item Views 
class ItemListView(LoginRequiredMixin, generic.ListView):
    model = Item

class ItemDetailView(LoginRequiredMixin, generic.DetailView):
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

def registerPage(request): 
    form = CreateUserForm(request.POST)

    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='employee')
        user.groups.add(group)
        employee = Employee.objects.create(user=user)
        employee.save()

        messages.success(request, 'Account was created for ' + username)
        return redirect('login')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)