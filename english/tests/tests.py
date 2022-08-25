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
        self.teacher = User.objects.get(id=2)

    def test_get_classes_list(self):
        self.client.force_login(user=self.student)
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

    def test_get_classes_success(self):
        self.client.force_login(user=self.student)
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

    def test_get_classes_failed(self):
        self.client.force_login(user=self.teacher)
        url = reverse("student-classes-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_leave_class(self):
        data = {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}

        self.client.force_login(user=self.teacher)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertIn(data, response.data["students"])

        self.client.force_login(user=self.student)
        url = reverse("join-to-class", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.force_login(user=self.teacher)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertNotIn(data, response.data["students"])

    def test_join_class(self):
        self.client.force_login(user=self.student)
        data = {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"}

        url = reverse("join-to-class", kwargs={"pk": 1})
        self.client.delete(url)
        url = f'{reverse("classes-list")}?name=FirstClass'
        response = self.client.get(url)
        self.assertNotIn(data, response.data[0]["students"])

        url = reverse("join-to-class", kwargs={"pk": 1})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(data, response.data["students"])


class ClassesForTeacher(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_classes_success(self):
        self.client.force_login(user=self.teacher)
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

    def test_get_classes_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-classes-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_classes_success(self):
        self.client.force_login(user=self.teacher)
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

    def test_search_classes_success_empty_results(self):
        self.client.force_login(user=self.teacher)
        url = f'{reverse("classes-list")}?name=LostClass'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_class_success(self):
        self.client.force_login(user=self.teacher)
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
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)

    def test_get_class_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_class_success(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "UpdatedFirstClass",
            "days": [1, 2],
            "start_time": "20:00:00",
            "end_time": "21:30:00"
        }
        expected_data = {
            "pk": 1,
            "name": "UpdatedFirstClass",
            "students": [
                {"pk": 1, "first_name": "Maksim", "last_name": "Lukash"},
                {"pk": 3, "first_name": "Ayden", "last_name": "Henris"},
                {"pk": 4, "first_name": "Damian", "last_name": "Ward"},
                {"pk": 5, "first_name": "Jonah", "last_name": "Matthews"}
            ],
            "teacher": {"pk": 2, "first_name": "Matthew", "last_name": "Becher"},
            "days": ["Tuesday", "Wednesday"],
            "start_time": "20:00:00",
            "end_time": "21:30:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(dict(response.data), expected_data)

    def test_update_class_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "name": "FailedUpdateFirstClass",
            "days": [3, 5]
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_class_failed_incorrect_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "FirstClass",
            "start_time": "22:00:00",
            "end_time": "20:00:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The start time can't be greater than the end time.", response.data["non_field_errors"])

    def test_update_class_failed_unfilled_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "FirstClass",
            "end_time": "20:00:00"
        }
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Please, fill in the start and end times.", response.data["non_field_errors"])

    def test_delete_class_success(self):
        self.client.force_login(user=self.teacher)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_class_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-classes-retrive-update-destroy", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_class_success(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "NewClass",
            "students": [4, 5],
            "days": [1, 2],
            "start_time": "16:00:00",
            "end_time": "18:00:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_class_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "name": "NewSecondClass",
            "students": [4, 5],
            "days": [1, 2],
            "start_time": "16:00:00",
            "end_time": "18:00:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_class_failed_incorrect_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "name": "NewSecondClass",
            "students": [4, 5],
            "days": [1, 2],
            "start_time": "20:00:00",
            "end_time": "18:00:00"
        }
        url = reverse("teacher-classes-list-create")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The start time can't be greater than the end time.", response.data["non_field_errors"])


class LessonsForStudent(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_lessons_success(self):
        self.client.force_login(user=self.student)
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

    def test_get_lessons_failed(self):
        self.client.force_login(user=self.teacher)
        url = reverse("student-lessons-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonsForTeacher(APITestCase):
    fixtures = [
        "english/tests/fixtures.json",
    ]

    def setUp(self):
        self.student = User.objects.get(id=1)
        self.teacher = User.objects.get(id=2)

    def test_get_lessons_success(self):
        self.client.force_login(user=self.teacher)
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

    def test_get_lessons_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-lessons-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_lesson_success(self):
        self.client.force_login(user=self.teacher)
        expected_data = {
            "pk": 1,
            "class_name": "FirstClass",
            "_status": "COMING",
            "time_start": "2030-07-04T01:14:43",
            "time_end": "2030-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertDictEqual(dict(response.data), expected_data)

    def test_get_lesson_failed(self):
        self.client.force_login(user=self.student)
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_success(self):
        self.client.force_login(user=self.teacher)
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
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        self.client.patch(url, data=data)
        url = reverse("teacher-lessons-list-create")
        response = self.client.get(url)
        self.assertDictEqual(dict(response.data[0]), expected_data)

    def test_update_lesson_failed_incorrect_time(self):
        self.client.force_login(user=self.teacher)
        data = {
            "time_start": "2050-07-04T01:14:43",
            "time_end": "2030-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The start time can't be greater than the end time.", response.data["non_field_errors"])

    def test_update_lesson_failed_403(self):
        self.client.force_login(user=self.student)
        data = {
            "time_start": "2030-07-04T01:14:43",
            "time_end": "2032-10-30T01:14:46"
        }
        url = reverse("teacher-lesson-retrive-update", kwargs={"pk": 1})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
