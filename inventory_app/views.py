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
import pandas as pd


def index(request):
# Render index.html
    return render( request, 'inventory_app/index.html')

class ItemListView (generic.ListView):
    model = Item

class ItemDetailView(generic.DetailView):
    model = Item

# Views that require login credentials. 
@login_required(login_url='login')
@allowed_users(allowed_roles='employee')
def userUpdate(request, pk):
    employee = request.user.employee
    form = EmployeeForm(instance=employee)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee information updated successfully')
            return redirect('user_page', pk=pk)  # Pass the pk parameter in the redirection
    
    context = {'form': form}
    return render(request, 'registration/user_update.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles='employee')
def addItem(request):
    form = ItemForm()

    if request.method == 'POST':
        # Create a new dictionary with form data
        item_data = request.POST.copy()
        
        form = ItemForm(item_data)
        if form.is_valid():
            # Save the form without committing to the database
            item = form.save(commit=False)
            # Save item to database
            item.save()

            # Redirect back to the inventory page
            return redirect('inventory')

    # Render the form template if the request method is GET
    context = {'form': form}
    return render(request, 'inventory_app/item_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='employee')
def deleteItem(request, pk):
    item = Item.objects.get(pk=pk)

    if request.method == 'POST':
        item.delete() 
        return redirect('inventory')
    
    context = {'item': item}
    return render(request, 'inventory_app/item_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='employee')
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


def registerPage(request): 
    form = CreateUserForm(request.POST)

    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='employee')
        user.groups.add(group)
        employee = Employee.objects.create(user = user)
        messages.success(request, 'Account was created for ' + username)
        return redirect('login')

    
    context = {'form': form}
    return render(request, 'registration/register.html', context)

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'registration/employee_detail.html'
    context_object_name = 'employee'
    model = Employee

@login_required(login_url='login')
@allowed_users(allowed_roles='employee')
def download_to_excel(request):
    # Retrieve all items
    items = Item.objects.all()

    # Create a Pandas DataFrame from the item data
    data = {
        'Name': [item.name for item in items],
        'Category': [item.category for item in items],
        'Cost': [item.cost for item in items],
        'Amount': [item.amount for item in items],
    }
    df = pd.DataFrame(data)

    # Create an Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_list.xlsx'

    # Write the DataFrame to the response
    df.to_excel(response, index=False)

    return response