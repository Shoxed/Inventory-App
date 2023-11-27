# IMPORTS FOR UNIT TESTS 
from django.test import TestCase, SimpleTestCase, LiveServerTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User, Group
from .models import *
from .views import *
from .forms import *

# IMPORTS FOR SELENIUM
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# UNITS TEST FOR MODELS, VIEWS, URLS, FORMS

# Test cases for authentication in the inventory app
class UserTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group, created = Group.objects.get_or_create(name='employee')
        self.user.groups.add(self.group)

    def test_register(self):
        # Test user registration view
        response = self.client.get(reverse('register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

        # Test registration with valid data
        new_user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'jshdwwdws',
            'password2': 'jshdwwdws'
        }
        response = self.client.post(reverse('register_page'), data=new_user_data)
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('login'))  # Redirects to the login page

        new_user_created = User.objects.filter(username='newuser').exists()
        self.assertTrue(new_user_created, "User not created.")
    
    def test_login(self):
        # Test user login view
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        # Test login with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

        # Check that the user is now authenticated
        self.assertTrue(response.client.session['_auth_user_id'])

    def test_logout(self):
        # Test user logout view
        self.client.login(username='testuser', password='testpass')  # Log in first
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200) 

        # Check that the user is now logged out
        self.assertNotIn('_auth_user_id', self.client.session)

# Test cases for views in the inventory app
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.group, created = Group.objects.get_or_create(name='employee')
        self.user.groups.add(self.group)
        self.employee = Employee.objects.create(
            user=self.user,
            name='Test Employee',
            position='Test Position'
        )
        self.item = Item.objects.create(
            name='Test Item',
            category='Test Category',
            cost=2.5,
            amount=10
        )
        self.client.login(username='testuser', password='testpass')


    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/index.html')

    def test_item_list_view(self):
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_list.html')

    def test_item_detail_view(self):
        response = self.client.get(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_detail.html')

    def test_user_update_view(self):
        response = self.client.get(reverse('user_update', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/user_update.html')

    def test_add_item_view(self):
        response = self.client.get(reverse('add-item'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_form.html')

    def test_delete_item_view(self):
        response = self.client.get(reverse('item-delete', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_delete.html')

    def test_update_item_view(self):
        response = self.client.get(reverse('item-update', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory_app/item_update.html')

    def test_register_page_view(self):
        response = self.client.get(reverse('register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_employee_detail_view(self):
        response = self.client.get(reverse('user_page', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/employee_detail.html')

    def test_download_to_excel_view(self):
        response = self.client.get(reverse('download-to-excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=inventory_list.xlsx')
        self.assertEqual(response.get('Content-Type'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertTrue(response.content)  # Check that the response has content

    def test_add_item_post_view(self):
        response = self.client.post(reverse('add-item'), {
            'name': 'New Test Item',
            'category': 'Bread',
            'cost': 3.0,
            'amount': 5,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST
        self.assertRedirects(response, reverse('inventory'))  # Redirects to the inventory page

        # Check that the new item is created
        new_item = Item.objects.get(name='New Test Item')
        self.assertEqual(new_item.category, 'Bread')
        self.assertEqual(new_item.cost, 3.0)
        self.assertEqual(new_item.amount, 5)

    def test_delete_item_post_view(self):
        response = self.client.post(reverse('item-delete', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST
        self.assertRedirects(response, reverse('inventory'))  # Redirects to the inventory page

        # Check that the item is deleted
        with self.assertRaises(Item.DoesNotExist):
            deleted_item = Item.objects.get(id=self.item.id)

    def test_update_item_post_view(self):
        response = self.client.post(reverse('item-update', args=[self.item.id]), {
            'name': 'Updated Test Item',
            'category': 'Bread',
            'cost': 4.0,
            'amount': 15,
        })

        # Check that the item is updated
        updated_item = Item.objects.get(id=self.item.id)
        self.assertEqual(updated_item.name, 'Updated Test Item')
        self.assertEqual(updated_item.category, 'Bread')
        self.assertEqual(updated_item.cost, 4.0)
        self.assertEqual(updated_item.amount, 15)

    def test_register_page_post_view(self):
        response = self.client.post(reverse('register_page'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'jshdwwdws',
            'password2': 'jshdwwdws',
        })

        # Check that the new user is created
        new_user = User.objects.get(username='newuser')
        self.assertTrue(new_user.check_password('jshdwwdws'))
        self.assertTrue(new_user.groups.filter(name='employee').exists())
        self.assertTrue(Employee.objects.filter(user=new_user).exists())

    def test_user_update_post_view(self):
        response = self.client.post(reverse('user_update', args=[self.user.id]), {
            'name': 'Updated Test Employee',
            'position': 'Updated Test Position',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful POST
        self.assertRedirects(response, reverse('user_page', args=[self.user.id]))  # Redirects to the user detail page

        # Check that the employee is updated
        updated_employee = Employee.objects.get(user=self.user)
        self.assertEqual(updated_employee.name, 'Updated Test Employee')
        self.assertEqual(updated_employee.position, 'Updated Test Position')

    def test_download_to_excel_post_view(self):
        response = self.client.post(reverse('download-to-excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename=inventory_list.xlsx')
        self.assertEqual(response.get('Content-Type'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertTrue(response.content)  # Check that the response has content

    def test_invalid_item_form_post_view(self):
        response = self.client.post(reverse('add-item'), {
            'name': '',  # Invalid data
            'category': 'Invalid Category',
            'cost': -1.0,  # Invalid data
            'amount': -5,  # Invalid data
        })
        self.assertEqual(response.status_code, 200)  # Form validation failed, should return to the form page
        self.assertTemplateUsed(response, 'inventory_app/item_form.html')

        # Check that the form errors are present in the response context
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

# Test cases for forms in the inventory app
class FormsTests(TestCase):

    def test_employee_form_valid(self):
        # Test the EmployeeForm with valid data
        form_data = {
            'name': 'Test Employee',
            'position': 'Test Position',
        }
        form = EmployeeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_employee_form_invalid(self):
        # Test the EmployeeForm with invalid data
        form_data = {
            'name': '',
            'position': 'Test Position',
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_item_form_valid(self):
        # Test the ItemForm with valid data
        form_data = {
            'name': 'Test Item',
            'category': 'Fruit',
            'cost': 2.5,
            'amount': 10,
        }
        form = ItemForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_item_form_invalid(self):
        # Test the ItemForm with invalid data
        form_data = {
            'name': '',
            'category': 'Test Category',
            'cost': 2.5,
            'amount': 10,
        }
        form = ItemForm(data=form_data)
        self.assertFalse(form.is_valid())

# Test cases for models in the inventory app
class ModelsTests(TestCase):
    def setUp(self):
        # Set up a test user, employee, and item for model testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            name='Test Employee',
            position='Test Position'
        )
        self.item = Item.objects.create(
            name = 'Test Item',
            category = 'Bread',
            cost = 2.5,
            amount = 10
        )

    def test_item_model(self):
        # Test the Item model
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(self.item.name, 'Test Item')
        self.assertEqual(self.item.category, 'Bread')
        self.assertEqual(self.item.cost, 2.5)
        self.assertEqual(self.item.amount, 10)

        # Test the get_absolute_url method
        expected_url = f'/inventory/{self.item.id}/'
        self.assertEqual(self.item.get_absolute_url(), expected_url)
    
    def test_employee_model(self):
        # Test the Employee model
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(self.employee.name, 'Test Employee')
        self.assertEqual(self.employee.position, 'Test Position')

        # Test the relationship between User and Employee
        user = self.employee.user
        self.assertIsNotNone(user)
        self.assertEqual(user.employee, self.employee)

        # Test the exclusion of 'user' field in EmployeeForm
        employee_form_fields = [field for field in EmployeeForm().fields]
        self.assertNotIn('user', employee_form_fields)

# Test cases for URLs in the inventory app
class UrlsTests(SimpleTestCase):

    def test_index_url(self):
        # Test the index URL
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_item_list_url(self):
        # Test the item list URL
        url = reverse('inventory')
        self.assertEqual(resolve(url).func.view_class, ItemListView)

    def test_item_detail_url(self):
        # Test the item detail URL
        url = reverse('item-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ItemDetailView)

    def test_user_update_url(self):
        # Test the user update URL
        url = reverse('user_update', args=[1])
        self.assertEqual(resolve(url).func, userUpdate)

    def test_add_item_url(self):
        # Test the add item URL
        url = reverse('add-item')
        self.assertEqual(resolve(url).func, addItem)

    def test_delete_item_url(self):
        # Test the delete item URL
        url = reverse('item-delete', args=[1])
        self.assertEqual(resolve(url).func, deleteItem)

    def test_update_item_url(self):
        # Test the update item URL
        url = reverse('item-update', args=[1])
        self.assertEqual(resolve(url).func, updateItem)

    def test_register_page_url(self):
        # Test the register page URL
        url = reverse('register_page')
        self.assertEqual(resolve(url).func, registerPage)

    def test_employee_detail_url(self):
        # Test the employee detail URL
        url = reverse('user_page', args=[1])
        self.assertEqual(resolve(url).func.view_class, EmployeeDetailView)

# SELENIUM WEBDRIVER TESTS

class SeleniumTests(LiveServerTestCase):
    def setUp(self):
        # Create a browser instance
        self.browser = webdriver.Chrome()

    def tearDown(self):
        # Close the browser
        self.browser.quit()
    
    def test_navbar(self):
        # The user goes to the home page of the blog
        self.browser.get("http://127.0.0.1:8000/")
        time.sleep(2)

        home_link = By.LINK_TEXT, "Home"
        inventory_link = By.LINK_TEXT, "Inventory"
        login_link = By.LINK_TEXT, "Login"
        logout_link = By.LINK_TEXT, "Logout"
        account_link = By.PARTIAL_LINK_TEXT, "Account"

        try:
            self.browser.find_element(*logout_link).click()
        except:
            print("Already logged out")
        time.sleep(1)
        self.browser.find_element(*inventory_link).click()
        time.sleep(1)
        self.browser.find_element(*home_link).click()
        time.sleep(1)
        self.browser.find_element(*login_link).click()
        time.sleep(1)
        self.browser.find_element(By.ID, 'id_username').send_keys('hixx')
        time.sleep(1)
        self.browser.find_element(By.ID, 'id_password').send_keys('jon2002sky')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        time.sleep(4)
        self.browser.find_element(*account_link).click()
    
    def test_login_failure(self):
        self.browser.get("http://127.0.0.1:8000/accounts/login/")
        time.sleep(1)
        self.browser.find_element(By.NAME, 'username').send_keys('invaliduser')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password').send_keys('InvalidPass123')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

        self.assertIn("Your username and password didn't match. Please try again.", self.browser.page_source)
    
    def test_registration(self):
        self.browser.get("http://127.0.0.1:8000/accounts/register/")
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('BruceWayne')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'email').send_keys('test@email.com')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password1').send_keys('qwerfvdsadf')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password2').send_keys('qwerfvdsadf')
        time.sleep(2)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    
    def test_create_item(self):
        self.browser.get("http://127.0.0.1:8000/accounts/login/")

        self.browser.find_element(By.NAME, 'username').send_keys('hixx')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'password').send_keys('jon2002sky')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        time.sleep(1)
        # Navigate to the add item page
        self.browser.get("http://127.0.0.1:8000/inventory/add_item/")

        self.browser.find_element(By.NAME, 'name').send_keys('Test Item')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'category').send_keys('Dairy')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'cost').send_keys('10.99')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'amount').send_keys('50')
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="Submit"]').click()