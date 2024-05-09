from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from myapp.views import send_sms
from .models import Customer, Order

class OrderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.customer = Customer.objects.create(
            name='testcustomer@example.com', code='ABCDE12345'
        )

    def test_create_order_view(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'customer': self.customer.name,
            'item': 'Test Item',
            'amount': 10.99,
            'phoneNumber': '+254712345678'
        }
        response = self.client.post(reverse('create_order'), data)
        self.assertEqual(response.status_code, 302)  # Redirect on successful order creation
        order = Order.objects.first()
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.item, 'Test Item')
        self.assertEqual(order.amount, Decimal('10.99'))        
        

    def test_delete_order_view(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(
            customer=self.customer, item='Test Item', amount=10.99
        )
        response = self.client.post(reverse('delete_order', args=[order.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_order_detail_view(self):
        order = Order.objects.create(
            customer=self.customer, item='Test Item', amount=10.99
        )
        response = self.client.get(reverse('order_detail', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, '10.99')

    def test_send_sms(self):
        # This test will only check if the function doesn't raise an exception
        # You may need to mock the AfricasTalking API to properly test the SMS sending functionality
        recipients = ['+254712345678']
        message = 'Test SMS'
        try:
            send_sms(message, recipients)
        except Exception as e:
            self.fail(f'send_sms raised an exception: {e}')