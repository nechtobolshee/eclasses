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
        self.client.force_login(user=self.testUser)

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
        url = reverse("classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_classes_for_current_student(self):
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
        url = reverse("student-my")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_classes_for_current_teacher(self):
        expected_data = {
            "pk": 2,
            "name": "SecondClass",
            "students": [
                {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Brody", "last_name": "Nelson"},
                {"pk": 5, "first_name": "Damian", "last_name": "Ward"},
            ],
            "teacher": {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
        }
        url = reverse("teacher-my")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_search_classes_with_filters(self):
        expected_data = {
            "pk": 3,
            "name": "ThirdClass",
            "students": [
                {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
                {"pk": 4, "first_name": "Brody", "last_name": "Nelson"},
                {"pk": 5, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
            ],
            "teacher": {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
        }
        url = f'{reverse("classes-list")}?name=&teacher=3&students=5'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)
