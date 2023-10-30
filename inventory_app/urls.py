from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.ItemListView.as_view(), name = "inventory"),
    path('inventory/<int:pk>', views.ItemDetailView.as_view(), name = 'item-detail'),
]