from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.ItemListView.as_view(), name = "inventory"),
    path('inventory/<int:pk>/', views.ItemDetailView.as_view(), name = 'item-detail'),
    path('inventory/add_item/', views.addItem, name='add-item'),
    path('inventory/delete_item/<int:pk>/', views.deleteItem, name='item-delete'),
    path('inventory/update_item/<int:pk>/', views.updateItem, name = 'item-update'),
]