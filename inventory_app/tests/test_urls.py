from django.test import TestCase
from django.urls import reverse, resolve
from inventory_app.views import index, ItemListView, ItemDetailView, addItem, deleteItem, updateItem

class TestUrls(TestCase):

    # Tests if URL path resolves to the correct view function
    def test_index_url_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)
    
    def test_add_item_url(self):
        url = reverse('add-item')
        self.assertEquals(resolve(url).func, addItem)
    
    def test_add_item_url(self):
        url = reverse('item-delete', args= ['some-int'])
        self.assertEquals(resolve(url).func, deleteItem)

    def test_add_item_url(self):
        url = reverse('item-update', args = ['some-int'])
        self.assertEquals(resolve(url).func, updateItem)

    # Tests if URL path resolves to correct view class
    def test_listView_url_resolves(self):
        url = reverse('inventory', )
        self.assertEquals(resolve(url).func.view_class, ItemListView)
    
    def test_detailView_url_resolves(self):
        url = reverse('item-detail', args = ['some-int'])
        self.assertEquals(resolve(url).func.view_class, ItemDetailView)