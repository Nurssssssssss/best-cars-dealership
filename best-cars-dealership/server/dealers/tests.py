from django.test import TestCase,Client
from django.contrib.auth.models import User
from .models import Dealer
class DealerTests(TestCase):
 def setUp(self):
  self.d=Dealer.objects.create(name='Test Dealer',city='Wichita',state='Kansas',address='1 Main St')
 def test_dealers(self):
  self.assertEqual(self.client.get('/api/dealers/?state=Kansas').json()['dealers'][0]['name'],'Test Dealer')
 def test_dealer_details(self):
  self.assertEqual(self.client.get(f'/api/dealers/{self.d.id}/').status_code,200)
 def test_sentiment(self):
  self.assertEqual(self.client.get('/api/analyze/?text=Fantastic%20services').json()['sentiment'],'positive')
 def test_login_logout(self):
  User.objects.create_user('tester',password='VeryStrongPassword456!')
  self.assertEqual(self.client.post('/api/login/',data='{"username":"tester","password":"VeryStrongPassword456!"}',content_type='application/json').status_code,200)
  self.assertEqual(self.client.post('/api/logout/',data='{}',content_type='application/json').status_code,200)
