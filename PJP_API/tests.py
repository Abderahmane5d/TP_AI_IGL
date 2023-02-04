from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *
from django.urls import reverse

# Create your tests here.


class TestMessageCreate(APITestCase):
    # test de la creation d un nouveau message
    url = "/message_create"

    def test_post_MessageCreate(self):
        data = {
            "content": "message content",
            "utilisateur": "user1@gmail.com",
            "destination": "user3@gmail.com"
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["content"], "message content")


class TestLogin(APITestCase):
    # test de login pour un utilisateur inexistant
    url = "/login"

    def test_post_Login(self):
        data = {
            "email": "utilisateurInexistant@gmail.com"
            # aucun utilisateur ne possede cette adresse email
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(result['email'], "no user")


class TestSignUp(APITestCase):
    # test de sign up d un nouveau utilisateur
    url = "/signup"

    def test_post_Login(self):
        data = {
            "nom": "nom test",
            "prenom": "prenom test",
            "adresse": "adresse test",
            "email": "emailtest@gmail.com",
            "telephone": "telephone test"
        }

        response = self.client.post(self.url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['email'], "emailtest@gmail.com")
