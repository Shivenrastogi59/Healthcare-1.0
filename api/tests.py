from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class AuthFlowTests(APITestCase):
    def test_register_and_login(self):
        reg_url = reverse("register")
        payload = {"name": "Tester", "email": "t@e.com", "password": "abcDEF123!"}
        r = self.client.post(reg_url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        login_url = reverse("token_obtain_pair")
        r = self.client.post(login_url, {"username": payload["email"],"password": payload["password"]}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("access", r.data)

class PatientCrudTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u@e.com",
        email="u@e.com", password="Pass12345")
        login_url = reverse("token_obtain_pair")
        r = self.client.post(login_url, {"username": "u@e.com", "password": "Pass12345"}, format="json")
        self.token = r.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_and_list_patient(self):
        create_url = reverse("patient-list")
        p = {"first_name":"John","last_name":"Doe","age":30,"gender":"male"}
        r = self.client.post(create_url, p, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        r = self.client.get(create_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data["results"]), 1)