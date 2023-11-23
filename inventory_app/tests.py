from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from inventory_app.models import Item, Employee

# Tests that covrt login and registation for users
class AuthenticationTests(TestCase):

    def setUp(self):
        # Set up a user and a group
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='employee')
        self.user.groups.add(self.group)

    def test_login(self):
        # Test that the login view renders successfully and authenticates a user
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        # Test login with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse('index'))  # Redirects to the index page

        # Check that the user is now authenticated
        self.assertTrue(response.client.session['_auth_user_id'])

    def test_register(self):
        # Test that the register view renders successfully and registers a new user
        response = self.client.get(reverse('register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

        # Test registration with valid data
        new_user_data = {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword', 'password2': 'newpassword'}
        response = self.client.post(reverse('register_page'), data=new_user_data)
        self.assertEqual(response.status_code, 200)

        # Check that the new user is not authenticated automatically
        self.assertFalse(response.client.session.get('_auth_user_id'))

# Tests Item model by creating an Object of that model
class ItemModelTest(TestCase):
    # Test Item model to make sure an object can be sucessfully be created from it. 
    def test_get_absolute_url(self):
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        self.assertEqual(item.get_absolute_url(), f'/inventory/{item.id}/')

# Tests all view classes anf functions 
class TestViews(TestCase):

    def setUp(self):
        # Set up a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='employee')
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='testpass')
    
    def test_index_view(self):
        # Test that the index view renders successfully and uses the correct template
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/index.html')
    
    def test_item_list_view(self):
        # Test that the item list view renders successfully and uses the correct template
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_list.html')
    
    def test_item_detail_view(self):
        # Test that the item detail view renders successfully, uses the correct template,
        # and passes the correct item to the template context
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        response = self.client.get(reverse('item-detail', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_detail.html')
        self.assertEqual(response.context['object'], item)
    
    def test_add_item_view(self):
        # Test that the add item view renders successfully and uses the correct template
        response = self.client.get(reverse('add-item'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_form.html')

        # Test form submission with valid data
        form_data = {'name': 'New Test Item', 'category': 'Dairy', 'cost': 3.0, 'amount': 5}
        response = self.client.post(reverse('add-item'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Test that the item was added to the database
        new_item = Item.objects.get(name='New Test Item')
        self.assertIsNotNone(new_item)
    
    def test_delete_item_view(self):
        # Test that the delete item view renders successfully, uses the correct template,
        # and passes the correct item to the template context
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        response = self.client.get(reverse('item-delete', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_delete.html')

        # Test form submission for item deletion
        response = self.client.post(reverse('item-delete', args=[item.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Test that the item was deleted from the database
        with self.assertRaises(Item.DoesNotExist):
            Item.objects.get(id=item.id)
    
    def test_update_item_view(self):
        # Test that the update item view renders successfully, uses the correct template,
        # and passes the correct item to the template context
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        response = self.client.get(reverse('item-update', args=[item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_update.html')

        # Test form submission with valid data
        updated_data = {'name': 'Updated Test Item', 'category': 'Fruit', 'cost': 4.0, 'amount': 8}
        response = self.client.post(reverse('item-update', args=[item.id]), data=updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission

        # Test that the item was updated in the database
        updated_item = Item.objects.get(id=item.id)
        self.assertEqual(updated_item.name, 'Updated Test Item')
        self.assertEqual(updated_item.category, 'Fruit')
        self.assertEqual(updated_item.cost, 4.0)
        self.assertEqual(updated_item.amount, 8)

    def test_user_page_view(self):
        # Test that the user page view renders successfully, uses the correct template, 
        # and handles employee information update correctly
        employee = Employee.objects.create(user=self.user, name='Barry Allen', position='Manager')
        response = self.client.get(reverse('user_update'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/user.html')

        # Test form submission with valid employee information update data
        updated_data = {'name': 'Bruce Wayne', 'position': 'Supervisor'}
        response = self.client.post(reverse('user_update'), data=updated_data)
        self.assertEqual(response.status_code, 302)

        # Test that the employee information was updated in the database
        updated_employee = Employee.objects.get(user=self.user)
        self.assertEqual(updated_employee.name, 'Bruce Wayne')
        self.assertEqual(updated_employee.position, 'Supervisor')

# Tests URLs to make sure they resolve to correct view 
class UrlsTest(TestCase):
    def test_index_url(self):
        # Test that the index URL resolves to the correct view 
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_item_list_url(self):
        # Test that the item list URL resolves to the correct view
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
    
    def test_item_detail_url(self):
        # Test that the item detail URL resolves to correct view 
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        response = self.client.get(reverse('item-detail', args = [item.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_add_item_url(self):
        # Test that the add item URL resolves to correct view 
        response = self.client.get(reverse('add-item'))
        self.assertEqual(response.status_code, 200)
        
    
    def test_del_item_url(self):
        # Test that the delete item URL resolves to correct view 
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        response = self.client.get(reverse('item-delete', args=[item.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_update_item_url(self):
        # Test that the update item URL resolves to correct view 
        item = Item.objects.create(name='Test Item', category='Bread', cost=2.5, amount=10)
        response = self.client.get(reverse('item-update', args=[item.id]))
        self.assertEqual(response.status_code, 200)


