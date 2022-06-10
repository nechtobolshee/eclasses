from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ClassesListTest(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.testUser = User.objects.get(id=1)

    def test_get_classes_list(self):
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Brody", "last_name": "Nelson"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
            ],
            "teacher": {"pk": 5, "first_name": "Damian", "last_name": "Ward"},
        }
        url = reverse("classes_list")
        self.client.force_login(user=self.testUser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertDictEqual(dict(response.data[0]), expected_data)
