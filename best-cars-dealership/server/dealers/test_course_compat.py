from django.test import TestCase
from django.contrib.auth.models import User
from dealers.models import Dealer, CarMake, CarModel


class CourseraEndpointsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dealer = Dealer.objects.create(
            name="Test Dealer", city="Wichita", state="Kansas",
            address="123 Main Street", zip_code="67202"
        )
        make = CarMake.objects.create(name="Toyota")
        CarModel.objects.create(make=make, name="Camry")
        cls.user = User.objects.create_user(username="student", password="ExamplePass123!")

    def test_dealers(self):
        response = self.client.get("/fetchDealers")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["state"], "Kansas")

    def test_dealer_by_id(self):
        response = self.client.get(f"/fetchDealer/{self.dealer.id}")
        self.assertEqual(response.json()["full_name"], "Test Dealer")

    def test_dealers_by_state(self):
        self.assertEqual(len(self.client.get("/fetchDealers/Kansas").json()), 1)

    def test_reviews(self):
        self.assertEqual(self.client.get(f"/fetchReviews/dealer/{self.dealer.id}").json(), [])

    def test_cars(self):
        self.assertEqual(self.client.get("/djangoapp/get_cars").json()["CarModels"][0]["CarModel"], "Camry")

    def test_sentiment(self):
        self.assertEqual(self.client.get("/analyze/Fantastic%20services").json()["sentiment"], "positive")

    def test_login_logout(self):
        import json
        response = self.client.post("/djangoapp/login", data=json.dumps({
            "userName": "student", "password": "ExamplePass123!"
        }), content_type="application/json")
        self.assertEqual(response.json()["status"], "Authenticated")
        self.assertEqual(self.client.get("/djangoapp/logout").json()["userName"], "")
