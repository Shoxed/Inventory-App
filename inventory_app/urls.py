from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.ItemListView.as_view(), name = "inventory"),
    path('inventory/<int:pk>/', views.ItemDetailView.as_view(), name = 'item-detail'),
    path('inventory/add_item/', views.addItem, name='add-item'),
    path('inventory/delete_item/<int:pk>/', views.deleteItem, name='item-delete'),
    path('inventory/update_item/<int:pk>/', views.updateItem, name = 'item-update'),

    path('download-to-excel/', views.download_to_excel, name='download-to-excel'),

    #user authentication 
    path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/register/', views.registerPage, name = 'register_page'),
    path('user/<int:pk>/', views.EmployeeDetailView.as_view(),  name = 'user_page'),
    path('user/update/<int:pk>/', views.userUpdate, name = 'user_update'),
]