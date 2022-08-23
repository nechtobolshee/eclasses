from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ClassesForStudent(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.client.force_login(user=self.student)

    def test_get_classes_list(self):
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_get_classes(self):
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("student-classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_leave_class(self):
        url = "http://0.0.0.0:8000/english/student/classes/1/join/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_join_class(self):
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"},
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = "http://0.0.0.0:8000/english/student/classes/1/join/"
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)


class ClassesForTeacher(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.teacher = User.objects.get(id=2)
        self.client.force_login(user=self.teacher)

    def test_get_classes(self):
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_search_classes(self):
        expected_data = {
            "pk": 1,
            "name": "FirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "18:00:00",
            "end_time": "19:30:00"
        }
        url = f'{reverse("classes-list")}?name=FirstClass&teacher=2&students=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

        bad_url = f'{reverse("classes-list")}?name=LostClass'
        empty_response = self.client.get(bad_url)
        self.assertEqual(len(empty_response.data), 0)

    def test_delete_class(self):
        url = "http://0.0.0.0:8000/english/teacher/classes/1/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LessonsForStudent(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.client.force_login(user=self.student)

    def test_get_lessons(self):
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "_status": "COMING",
            "time_start": "2030-07-04T01:14:43",
            "time_end": "2030-10-30T01:14:46"
        }
        url = reverse("student-lessons-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertDictEqual(dict(response.data[0]), expected_data)


class LessonsForTeacher(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.teacher = User.objects.get(id=2)
        self.client.force_login(user=self.teacher)

    def test_get_lessons(self):
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "_status": "COMING",
            "time_start": "2030-07-04T01:14:43",
            "time_end": "2030-10-30T01:14:46"
        }
        url = reverse("teacher-lessons-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_update_lesson(self):
        data = {
            "time_start": "2030-07-04T01:14:43",
            "time_end": "2032-10-30T01:14:46"
        }
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "_status": "COMING",
            "time_start": "2030-07-04T01:14:43",
            "time_end": "2032-10-30T01:14:46"
        }
        url = "http://0.0.0.0:8000/english/teacher/lessons/1/"
        self.client.patch(url, data=data)
        url = reverse("teacher-lessons-list-create")
        response = self.client.get(url)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_update_lesson_bad_data(self):
        data = {
            "time_start": "2050-07-04T01:14:43",
            "time_end": "2030-10-30T01:14:46"
        }
        url = "http://0.0.0.0:8000/english/teacher/lessons/1/"
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

